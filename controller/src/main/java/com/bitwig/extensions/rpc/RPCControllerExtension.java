package com.bitwig.extensions.rpc;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;

import com.bitwig.extension.controller.ControllerExtension;
import com.bitwig.extension.controller.api.Application;
import com.bitwig.extension.controller.api.ControllerHost;
import com.bitwig.extension.controller.api.RemoteConnection;
import com.bitwig.extension.controller.api.Track;
import com.bitwig.extension.controller.api.TrackBank;

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
    public static final String VERSION = "0.3.1";

    private ControllerHost host;
    private Application application;
    private TrackBank trackBank;

    // Connection to MCP server
    private RemoteConnection mcpConnection;

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
        host.println("[init] Creating trackBank...");
        trackBank = host.createTrackBank(8, 0, 8);

        // Mark project name as interested
        host.println("[init] Marking interests...");
        application.projectName().markInterested();

        // Mark all track properties as interested so we get updates
        for (int i = 0; i < 8; i++) {
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
        }

        // Connect to MCP server as client
        host.println("[init] Connecting to MCP server at " + MCP_HOST + ":" + MCP_PORT + "...");
        connectToMcpServer();

        host.showPopupNotification("RPC v" + VERSION + " connecting to MCP server");
    }

    private void connectToMcpServer() {
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
        host.println("[mcp] Response: " + response);

        // Send response with length prefix (MCP server expects framing)
        sendResponse(response);
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

        for (int i = 0; i < 8; i++) {
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

            sb.append(String.format(
                "{\"id\":%d,\"name\":\"%s\",\"type\":\"%s\",\"volume\":%.3f,\"pan\":%.3f,\"mute\":%b,\"solo\":%b,\"arm\":%b}",
                i,
                escapeJson(name != null ? name : ""),
                escapeJson(trackType != null ? trackType.toLowerCase() : ""),
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

    private String extractString(String json, String key) {
        String search = "\"" + key + "\":\"";
        int start = json.indexOf(search);
        if (start < 0) return "";
        start += search.length();
        int end = json.indexOf("\"", start);
        if (end < 0) return "";
        return json.substring(start, end);
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

    @Override
    public void exit() {
        host.println("RPC Controller shutting down");
    }

    @Override
    public void flush() {
        // Called regularly - can be used for sending updates
    }
}
