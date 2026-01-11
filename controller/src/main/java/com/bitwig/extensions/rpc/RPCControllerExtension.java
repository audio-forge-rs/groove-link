package com.bitwig.extensions.rpc;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import com.bitwig.extension.controller.ControllerExtension;
import com.bitwig.extension.controller.api.Application;
import com.bitwig.extension.controller.api.ControllerHost;
import com.bitwig.extension.controller.api.CursorTrack;
import com.bitwig.extension.controller.api.InsertionPoint;
import com.bitwig.extension.controller.api.RemoteConnection;
import com.bitwig.extension.controller.api.ClipLauncherSlotBank;
import com.bitwig.extension.controller.api.ClipLauncherSlotOrScene;
import com.bitwig.extension.controller.api.Track;
import com.bitwig.extension.controller.api.TrackBank;
import com.bitwig.extension.controller.api.Transport;

/**
 * Bitwig controller extension that connects to the MCP server as a TCP client.
 *
 * Architecture:
 * - MCP server (Rust) listens on port 8417
 * - This extension connects OUT to the MCP server
 * - MCP server sends JSON-RPC requests, we respond
 *
 * This inverted architecture works around Bitwig's broken RemoteSocket receive callback.
 */
public class RPCControllerExtension extends ControllerExtension {

    private static final String MCP_HOST = "localhost";
    private static final int MCP_PORT = 8417;
    public static final String VERSION = "0.5.2";

    private ControllerHost host;
    private Application application;
    private TrackBank trackBank;
    private CursorTrack cursorTrack;
    private Transport transport;

    // Connection to MCP server
    private RemoteConnection mcpConnection;

    // Pending operation state for async device insertion
    private List<DeviceSpec> pendingDevices;
    private int currentDeviceIndex;
    private String pendingRequestId;
    private String pendingTrackName;
    private int devicesAdded;

    protected RPCControllerExtension(
            RPCControllerExtensionDefinition definition,
            ControllerHost host) {
        super(definition, host);
        this.host = host;
    }

    @Override
    public void init() {
        host.println("RPC Controller v" + VERSION + " initializing...");
        host.println("[init] New architecture: connecting to MCP server as client");

        // Get Bitwig API objects
        host.println("[init] Creating application...");
        application = host.createApplication();

        // Use hierarchical track bank (hasFlatTrackList=false) for proper group representation
        // When false: operates on direct child tracks, not all nested tracks
        // This is better for representing nested tracks in groups
        host.println("[init] Creating hierarchical trackBank...");
        trackBank = host.createTrackBank(16, 0, 8, false);

        host.println("[init] Creating cursorTrack...");
        cursorTrack = host.createCursorTrack(0, 0);

        host.println("[init] Creating transport...");
        transport = host.createTransport();

        // Mark project name as interested
        host.println("[init] Marking interests...");
        application.projectName().markInterested();
        cursorTrack.name().markInterested();
        cursorTrack.exists().markInterested();
        cursorTrack.trackType().markInterested();

        // Mark all track properties as interested so we get updates
        for (int i = 0; i < 16; i++) {
            Track track = (Track) trackBank.getItemAt(i);
            track.name().markInterested();
            track.color().markInterested();
            track.volume().markInterested();
            track.pan().markInterested();
            track.mute().markInterested();
            track.solo().markInterested();
            track.arm().markInterested();
            track.exists().markInterested();
            track.trackType().markInterested();
            track.isGroup().markInterested();
        }

        // Connect to MCP server as client
        host.println("[init] Connecting to MCP server at " + MCP_HOST + ":" + MCP_PORT + "...");
        connectToMcpServer();

        host.showPopupNotification("RPC v" + VERSION + " connecting to MCP server");
    }

    private void connectToMcpServer() {
        host.println("[mcp] Attempting connection to " + MCP_HOST + ":" + MCP_PORT + "...");

        host.connectToRemoteHost(MCP_HOST, MCP_PORT, connection -> {
            host.println("[mcp] Connected to MCP server!");
            mcpConnection = connection;

            connection.setReceiveCallback(data -> {
                host.println("[mcp] Received " + data.length + " bytes: " + bytesToHex(data, 20));
                onDataReceived(data);
            });

            connection.setDisconnectCallback(() -> {
                host.println("[mcp] Disconnected from MCP server");
                mcpConnection = null;
                // Try to reconnect after a delay
                host.scheduleTask(this::connectToMcpServer, 5000);
            });
        });

        // If connection fails silently (server not running), callback never fires.
        // Schedule a check - if still not connected after 5 seconds, retry.
        host.scheduleTask(() -> {
            if (mcpConnection == null) {
                host.println("[mcp] Connection attempt timed out, retrying...");
                connectToMcpServer();
            }
        }, 5000);
    }

    private static String bytesToHex(byte[] bytes, int len) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < Math.min(bytes.length, len); i++) {
            sb.append(String.format("%02x", bytes[i]));
        }
        return sb.toString();
    }

    private void onDataReceived(byte[] data) {
        // In client mode, Bitwig's API automatically handles framing and delivers
        // complete JSON messages without the length prefix. So we just process
        // each callback as a complete request.
        //
        // Note: We still need to SEND length-prefixed responses because the MCP
        // server expects framed data.

        String request = new String(data, StandardCharsets.UTF_8);
        host.println("[mcp] Request (" + data.length + " bytes): " + request);

        String response = handleRequest(request);
        if (response != null) {
            host.println("[mcp] Response: " + response);
            sendResponse(response);
        }
        // null response means async operation in progress
    }

    private void sendResponse(String response) {
        if (mcpConnection == null) {
            host.errorln("[mcp] Cannot send response: not connected");
            return;
        }

        try {
            byte[] responseBytes = response.getBytes(StandardCharsets.UTF_8);
            ByteBuffer responseBuffer = ByteBuffer.allocate(4 + responseBytes.length);
            responseBuffer.putInt(responseBytes.length);
            responseBuffer.put(responseBytes);
            host.println("[mcp] Sending " + responseBuffer.array().length + " bytes");
            mcpConnection.send(responseBuffer.array());
        } catch (Exception e) {
            host.errorln("[mcp] Failed to send response: " + e.getMessage());
        }
    }

    /** Send a progress notification (no id) */
    private void sendProgress(int step, int total, String message) {
        String notification = String.format(
            "{\"jsonrpc\":\"2.0\",\"method\":\"progress\",\"params\":{\"step\":%d,\"total\":%d,\"message\":\"%s\"}}",
            step, total, escapeJson(message)
        );
        sendResponse(notification);
    }

    private String handleRequest(String requestJson) {
        try {
            // Simple JSON parsing without dependencies
            if (requestJson.trim().startsWith("[")) {
                // Batch request
                return handleBatchRequest(requestJson);
            } else {
                // Single request
                return handleSingleRequest(requestJson);
            }
        } catch (Exception e) {
            host.errorln("Error handling request: " + e.getMessage());
            return "{\"jsonrpc\":\"2.0\",\"error\":{\"code\":-32603,\"message\":\"Internal error\"},\"id\":null}";
        }
    }

    private String handleSingleRequest(String requestJson) {
        // Parse request (simple parsing)
        String method = extractString(requestJson, "method");
        String idStr = extractId(requestJson);

        // Handle methods that need params
        if (method.equals("track.create")) {
            return handleTrackCreate(requestJson, idStr);
        }
        if (method.equals("transport.setTempo")) {
            return handleSetTempo(requestJson, idStr);
        }
        if (method.equals("clip.insertFile")) {
            return handleClipInsertFile(requestJson, idStr);
        }

        String result = dispatchMethod(method);

        if (result.startsWith("{\"error\":")) {
            return "{\"jsonrpc\":\"2.0\"," + result.substring(1, result.length() - 1) + ",\"id\":" + idStr + "}";
        }
        return "{\"jsonrpc\":\"2.0\",\"result\":" + result + ",\"id\":" + idStr + "}";
    }

    private String handleBatchRequest(String requestJson) {
        StringBuilder responses = new StringBuilder("[");
        // Simple batch parsing - split by },{ pattern
        String[] requests = requestJson.substring(1, requestJson.length() - 1).split("\\},\\s*\\{");

        for (int i = 0; i < requests.length; i++) {
            String req = requests[i];
            if (!req.startsWith("{")) req = "{" + req;
            if (!req.endsWith("}")) req = req + "}";

            if (i > 0) responses.append(",");
            responses.append(handleSingleRequest(req));
        }

        responses.append("]");
        return responses.toString();
    }

    private String dispatchMethod(String method) {
        switch (method) {
            case "info.get":
                return getInfo();
            case "list.tracks":
                return listTracks();
            case "list.scenes":
                return listScenes();
            default:
                return "{\"error\":{\"code\":-32601,\"message\":\"Method not found: " + method + "\"}}";
        }
    }

    // ==================== Transport Control ====================

    /**
     * Handle transport.setTempo method.
     *
     * Params:
     *   bpm: number - tempo in beats per minute (20-666)
     */
    private String handleSetTempo(String requestJson, String idStr) {
        try {
            double bpm = extractDouble(requestJson, "bpm");
            if (bpm < 20 || bpm > 666) {
                return formatError(idStr, -32602, "Tempo must be between 20 and 666 BPM");
            }

            host.println("[transport.setTempo] Setting tempo to " + bpm + " BPM");
            transport.tempo().setRaw(bpm);

            return formatResult(idStr, String.format("{\"bpm\":%.1f}", bpm));
        } catch (Exception e) {
            host.errorln("[transport.setTempo] Error: " + e.getMessage());
            return formatError(idStr, -32603, "Error setting tempo: " + e.getMessage());
        }
    }

    /**
     * Handle clip.insertFile method - insert file into clip launcher slot.
     *
     * Params:
     *   trackIndex: int - track index (0-based)
     *   slotIndex: int - clip launcher slot index (0-based)
     *   path: string - absolute path to file (MIDI, audio, etc.)
     */
    private String handleClipInsertFile(String requestJson, String idStr) {
        try {
            int trackIndex = extractInt(requestJson, "trackIndex");
            int slotIndex = extractInt(requestJson, "slotIndex");
            String path = extractString(requestJson, "path");

            if (path.isEmpty()) {
                return formatError(idStr, -32602, "Missing 'path' parameter");
            }

            host.println("[clip.insertFile] track=" + trackIndex + ", slot=" + slotIndex + ", path=" + path);

            // Get the track and clip launcher slot
            Track track = (Track) trackBank.getItemAt(trackIndex);
            if (!track.exists().get()) {
                return formatError(idStr, -32602, "Track " + trackIndex + " does not exist");
            }

            ClipLauncherSlotBank slotBank = track.clipLauncherSlotBank();
            ClipLauncherSlotOrScene slot = (ClipLauncherSlotOrScene) slotBank.getItemAt(slotIndex);

            // Insert the file using the slot's insertion point
            InsertionPoint insertionPoint = slot.replaceInsertionPoint();
            insertionPoint.insertFile(path);

            return formatResult(idStr, String.format(
                "{\"trackIndex\":%d,\"slotIndex\":%d,\"path\":\"%s\"}",
                trackIndex, slotIndex, escapeJson(path)
            ));
        } catch (Exception e) {
            host.errorln("[clip.insertFile] Error: " + e.getMessage());
            return formatError(idStr, -32603, "Error inserting file: " + e.getMessage());
        }
    }

    // ==================== Track Creation ====================

    /**
     * Handle track.create method with optional device loading.
     *
     * Params:
     *   name: string - track name
     *   type: string - "instrument", "audio", or "effect"
     *   devices: array of {type: "file"|"vst3"|"clap", path/id: string}
     */
    private String handleTrackCreate(String requestJson, String idStr) {
        try {
            // Extract params object first to avoid matching nested "type" in devices
            String paramsJson = extractParamsObject(requestJson);
            String trackName = extractString(paramsJson, "name");
            String trackType = extractTopLevelString(paramsJson, "type");
            List<DeviceSpec> devices = extractDevices(requestJson);

            host.println("[track.create] name=" + trackName + ", type=" + trackType + ", devices=" + devices.size());

            // Send initial progress
            int totalSteps = 1 + devices.size();
            sendProgress(1, totalSteps, "Creating track '" + trackName + "'");

            // Create the track
            int position = -1; // -1 = at end
            switch (trackType.toLowerCase()) {
                case "instrument":
                    application.createInstrumentTrack(position);
                    break;
                case "audio":
                    application.createAudioTrack(position);
                    break;
                case "effect":
                    application.createEffectTrack(position);
                    break;
                default:
                    return formatError(idStr, -32602, "Invalid track type: " + trackType);
            }

            // If no devices, we're done immediately
            if (devices.isEmpty()) {
                // Schedule name setting after track is created
                host.scheduleTask(() -> {
                    if (trackName != null && !trackName.isEmpty()) {
                        cursorTrack.name().set(trackName);
                    }
                }, 100);

                return formatResult(idStr, String.format(
                    "{\"trackName\":\"%s\",\"type\":\"%s\",\"devicesAdded\":0}",
                    escapeJson(trackName), escapeJson(trackType)
                ));
            }

            // Store state for async device insertion
            this.pendingDevices = devices;
            this.currentDeviceIndex = 0;
            this.pendingRequestId = idStr;
            this.pendingTrackName = trackName;
            this.devicesAdded = 0;

            // Schedule device insertion after track is created and selected
            // Give Bitwig time to create the track and select it
            host.scheduleTask(() -> {
                if (trackName != null && !trackName.isEmpty()) {
                    cursorTrack.name().set(trackName);
                }
                // Start inserting devices
                host.scheduleTask(this::insertNextDevice, 100);
            }, 200);

            // Return null to indicate async response
            return null;

        } catch (Exception e) {
            host.errorln("[track.create] Error: " + e.getMessage());
            return formatError(idStr, -32603, "Error creating track: " + e.getMessage());
        }
    }

    /** Insert the next device in the pending list */
    private void insertNextDevice() {
        if (pendingDevices == null || currentDeviceIndex >= pendingDevices.size()) {
            // All done - send final response
            sendFinalTrackResponse();
            return;
        }

        DeviceSpec device = pendingDevices.get(currentDeviceIndex);
        int totalSteps = 1 + pendingDevices.size();
        int step = 2 + currentDeviceIndex;

        host.println("[device] Inserting device " + (currentDeviceIndex + 1) + "/" + pendingDevices.size() +
                     ": type=" + device.type + ", path=" + device.path);

        sendProgress(step, totalSteps, "Adding " + device.getDisplayName());

        // Get insertion point at end of device chain
        InsertionPoint insertionPoint = cursorTrack.endOfDeviceChainInsertionPoint();

        try {
            switch (device.type) {
                case "file":
                    // Insert preset file
                    insertionPoint.insertFile(device.path);
                    devicesAdded++;
                    break;
                case "vst3":
                    // Insert VST3 plugin
                    insertionPoint.insertVST3Device(device.path);
                    devicesAdded++;
                    break;
                case "clap":
                    // Insert CLAP plugin
                    insertionPoint.insertCLAPDevice(device.path);
                    devicesAdded++;
                    break;
                case "vst2":
                    // VST2 needs int ID, parse it
                    try {
                        int vst2Id = Integer.parseInt(device.path);
                        insertionPoint.insertVST2Device(vst2Id);
                        devicesAdded++;
                    } catch (NumberFormatException e) {
                        host.errorln("[device] Invalid VST2 ID: " + device.path);
                    }
                    break;
                default:
                    host.errorln("[device] Unknown device type: " + device.type);
            }
        } catch (Exception e) {
            host.errorln("[device] Error inserting device: " + e.getMessage());
        }

        currentDeviceIndex++;

        // Schedule next device with delay to let Bitwig process
        host.scheduleTask(this::insertNextDevice, 150);
    }

    /** Send the final response after all devices are inserted */
    private void sendFinalTrackResponse() {
        String result = String.format(
            "{\"trackName\":\"%s\",\"devicesAdded\":%d}",
            escapeJson(pendingTrackName != null ? pendingTrackName : ""),
            devicesAdded
        );

        String response = formatResult(pendingRequestId, result);
        sendResponse(response);

        // Clear state
        pendingDevices = null;
        currentDeviceIndex = 0;
        pendingRequestId = null;
        pendingTrackName = null;
        devicesAdded = 0;
    }

    // ==================== Device Spec Parsing ====================

    private static class DeviceSpec {
        String type;  // "file", "vst3", "clap", "vst2"
        String path;  // file path or plugin ID

        String getDisplayName() {
            if (path == null) return type;
            // Extract filename from path
            int lastSlash = Math.max(path.lastIndexOf('/'), path.lastIndexOf('\\'));
            String name = lastSlash >= 0 ? path.substring(lastSlash + 1) : path;
            // Remove extension
            int lastDot = name.lastIndexOf('.');
            if (lastDot > 0) name = name.substring(0, lastDot);
            return name;
        }
    }

    /** Extract devices array from JSON request */
    private List<DeviceSpec> extractDevices(String json) {
        List<DeviceSpec> devices = new ArrayList<>();

        // Find devices array
        int start = json.indexOf("\"devices\"");
        if (start < 0) return devices;

        // Find opening bracket
        int arrayStart = json.indexOf('[', start);
        if (arrayStart < 0) return devices;

        // Find matching closing bracket
        int depth = 1;
        int pos = arrayStart + 1;
        int objStart = -1;

        while (pos < json.length() && depth > 0) {
            char c = json.charAt(pos);
            if (c == '[') depth++;
            else if (c == ']') depth--;
            else if (c == '{' && depth == 1) objStart = pos;
            else if (c == '}' && depth == 1 && objStart >= 0) {
                // Extract this device object
                String deviceJson = json.substring(objStart, pos + 1);
                DeviceSpec spec = parseDeviceSpec(deviceJson);
                if (spec != null) devices.add(spec);
                objStart = -1;
            }
            pos++;
        }

        return devices;
    }

    /** Parse a single device spec from JSON */
    private DeviceSpec parseDeviceSpec(String json) {
        DeviceSpec spec = new DeviceSpec();
        spec.type = extractString(json, "type");
        spec.path = extractString(json, "path");
        if (spec.path.isEmpty()) {
            spec.path = extractString(json, "id");
        }
        if (spec.type.isEmpty() || spec.path.isEmpty()) {
            return null;
        }
        return spec;
    }

    // ==================== Existing Methods ====================

    private String getInfo() {
        String bitwigVersion = host.getHostVersion();
        int apiVersion = host.getHostApiVersion();
        String platform = host.getPlatformType().name().toLowerCase();
        String projectName = application.projectName().get();
        if (projectName == null) projectName = "";

        return String.format(
            "{\"controllerVersion\":\"%s\",\"bitwigVersion\":\"%s\",\"apiVersion\":%d,\"platform\":\"%s\",\"projectName\":\"%s\"}",
            VERSION,
            escapeJson(bitwigVersion),
            apiVersion,
            platform,
            escapeJson(projectName)
        );
    }

    private String listTracks() {
        StringBuilder sb = new StringBuilder("[");
        boolean first = true;

        for (int i = 0; i < 16; i++) {
            Track track = (Track) trackBank.getItemAt(i);
            if (!track.exists().get()) continue;

            if (!first) sb.append(",");
            first = false;

            String name = track.name().get();
            String trackType = track.trackType().get();
            double volume = track.volume().get();
            double pan = track.pan().get();
            boolean mute = track.mute().get();
            boolean solo = track.solo().get();
            boolean arm = track.arm().get();
            boolean isGroup = track.isGroup().get();

            sb.append(String.format(
                "{\"id\":%d,\"name\":\"%s\",\"type\":\"%s\",\"isGroup\":%b,\"volume\":%.3f,\"pan\":%.3f,\"mute\":%b,\"solo\":%b,\"arm\":%b}",
                i,
                escapeJson(name != null ? name : ""),
                escapeJson(trackType != null ? trackType.toLowerCase() : ""),
                isGroup,
                volume,
                pan,
                mute,
                solo,
                arm
            ));
        }

        sb.append("]");
        return sb.toString();
    }

    private String listScenes() {
        // For now return empty - scenes need SceneBank
        return "[]";
    }

    // ==================== JSON Helpers ====================

    /** Extract the params object from a JSON-RPC request */
    private String extractParamsObject(String json) {
        int start = json.indexOf("\"params\"");
        if (start < 0) return json;

        // Find the opening brace
        int braceStart = json.indexOf('{', start);
        if (braceStart < 0) return json;

        // Find matching closing brace
        int depth = 1;
        int pos = braceStart + 1;
        while (pos < json.length() && depth > 0) {
            char c = json.charAt(pos);
            if (c == '{') depth++;
            else if (c == '}') depth--;
            pos++;
        }

        return json.substring(braceStart, pos);
    }

    /** Extract a top-level string value, skipping matches inside arrays */
    private String extractTopLevelString(String json, String key) {
        String search = "\"" + key + "\":\"";
        int searchFrom = 0;

        while (true) {
            int start = json.indexOf(search, searchFrom);
            if (start < 0) return "";

            // Check if this match is inside an array
            String before = json.substring(0, start);
            int lastOpen = before.lastIndexOf('[');
            int lastClose = before.lastIndexOf(']');

            if (lastOpen > lastClose) {
                // We're inside an array, skip this match and continue searching
                searchFrom = start + 1;
                continue;
            }

            // Found a top-level match
            start += search.length();
            int end = json.indexOf("\"", start);
            if (end < 0) return "";
            return unescapeJson(json.substring(start, end));
        }
    }

    private String extractString(String json, String key) {
        String search = "\"" + key + "\":\"";
        int start = json.indexOf(search);
        if (start < 0) return "";
        start += search.length();
        int end = json.indexOf("\"", start);
        if (end < 0) return "";
        return unescapeJson(json.substring(start, end));
    }

    private double extractDouble(String json, String key) {
        String search = "\"" + key + "\":";
        int start = json.indexOf(search);
        if (start < 0) return 0.0;
        start += search.length();

        // Skip whitespace
        while (start < json.length() && Character.isWhitespace(json.charAt(start))) {
            start++;
        }

        // Find end of number
        int end = start;
        while (end < json.length()) {
            char c = json.charAt(end);
            if (!Character.isDigit(c) && c != '.' && c != '-' && c != '+' && c != 'e' && c != 'E') break;
            end++;
        }

        if (end == start) return 0.0;
        try {
            return Double.parseDouble(json.substring(start, end));
        } catch (NumberFormatException e) {
            return 0.0;
        }
    }

    private int extractInt(String json, String key) {
        String search = "\"" + key + "\":";
        int start = json.indexOf(search);
        if (start < 0) return 0;
        start += search.length();

        // Skip whitespace
        while (start < json.length() && Character.isWhitespace(json.charAt(start))) {
            start++;
        }

        // Find end of number
        int end = start;
        while (end < json.length()) {
            char c = json.charAt(end);
            if (!Character.isDigit(c) && c != '-') break;
            end++;
        }

        if (end == start) return 0;
        try {
            return Integer.parseInt(json.substring(start, end));
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    private String extractId(String json) {
        String search = "\"id\":";
        int start = json.indexOf(search);
        if (start < 0) return "null";
        start += search.length();

        // Skip whitespace
        while (start < json.length() && Character.isWhitespace(json.charAt(start))) {
            start++;
        }

        // Find end of value
        int end = start;
        while (end < json.length()) {
            char c = json.charAt(end);
            if (c == ',' || c == '}' || Character.isWhitespace(c)) break;
            end++;
        }

        return json.substring(start, end);
    }

    private String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }

    private String unescapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\\"", "\"")
                .replace("\\\\", "\\")
                .replace("\\n", "\n")
                .replace("\\r", "\r")
                .replace("\\t", "\t");
    }

    private String formatResult(String id, String result) {
        return "{\"jsonrpc\":\"2.0\",\"result\":" + result + ",\"id\":" + id + "}";
    }

    private String formatError(String id, int code, String message) {
        return String.format(
            "{\"jsonrpc\":\"2.0\",\"error\":{\"code\":%d,\"message\":\"%s\"},\"id\":%s}",
            code, escapeJson(message), id
        );
    }

    @Override
    public void exit() {
        host.println("RPC Controller shutting down");
    }

    @Override
    public void flush() {
        // Called regularly - can be used for sending updates
    }
}
