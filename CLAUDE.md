# CLAUDE.md

## Project Overview

A Bitwig Studio controller extension with dual protocol interfaces:

- **JSON-RPC 2.0 over TCP** - For discrete, "offline" operations
  - Add/remove tracks
  - Load presets/devices
  - Project management
  - Browser operations
  - Batched commands with ACKs

- **OSC over UDP** - For real-time, continuous control
  - Volume/pan adjustments
  - Parameter tweaks
  - Transport control
  - Fader movements

This split leverages each protocol's strengths: JSON-RPC provides request/response semantics with batching, OSC provides low-latency fire-and-forget messaging.

## Documentation

### Bitwig Control Surface API Reference
- **Start here:** `docs/INDEX-bitwig-control-surface-api.md` - Quick reference tables with line numbers
- **Full API:** `docs/bitwig-control-surface-api.md` (1.7MB, 114K lines)
- Use line numbers from the index to read specific sections with offset/limit

**Key Classes:**
| Class | Purpose |
|-------|---------|
| `ControllerExtension` | Base class for controller extensions |
| `ControllerHost` | Main interface to Bitwig Studio |
| `Transport` | Play, stop, record, tempo, time signature |
| `Track` / `TrackBank` | Track properties and navigation |
| `CursorTrack` | Currently selected track |
| `Device` / `CursorDevice` | Device control and parameters |
| `Clip` / `CursorClip` | Clip properties and note data |
| `MidiIn` / `MidiOut` | MIDI I/O |
| `OscModule` / `OscServer` | OSC server for network control |

### Bitwig User Guide
- **Start here:** `docs/INDEX-bitwig-user-guide.md` - Topic lookup with section references
- **Full guide:** `docs/bitwig-user-guide.md` (806K, 29K lines)
- Covers Bitwig UI, workflow, all devices and Grid modules

## Development

### Controller Extension Structure
Bitwig controller extensions are Java-based. Key files:
- Extension definition class (metadata: name, author, UUID, MIDI ports)
- Extension class (init, exit, flush methods)

### API Patterns
```java
// Get host and create objects
ControllerHost host = getHost();
Transport transport = host.createTransport();
TrackBank trackBank = host.createTrackBank(8, 0, 0);

// Observe values
transport.isPlaying().addValueObserver(isPlaying -> {
    // React to transport state
});

// Control Bitwig
transport.play();
transport.stop();
track.volume().set(0.5);
```

### Critical: init() Constraints

**ALL `host.create*()` methods MUST be called during `init()`** (line 18381 in API docs)

This includes:
- `createRemoteConnection()` - TCP socket server
- `createTrackBank()` - Track access
- `createTransport()` - Transport control
- `createApplication()` - Application API
- `createNoteInput()` - explicitly documented (line 76563)
- All other `create*` methods on ControllerHost

If you call `create*` methods from `scheduleTask()` or elsewhere, you get:
```
Exception: Trying to create section outside of init().
```

**Pattern:** Create everything in `init()`, use callbacks/observers for runtime behavior.

### Service Discovery File

Bitwig discovers extensions via Java ServiceLoader. Required file:
```
META-INF/services/com.bitwig.extension.ExtensionDefinition
```

Contents (one class per line):
```
com.bitwig.extensions.rpc.RPCControllerExtensionDefinition
```

**Wrong filename:** `com.bitwig.extension.controller.ControllerExtensionDefinition` (this won't work)

## Architecture

### Current Design: MCP Server with Inverted TCP

Bitwig's `RemoteSocket` API has a bug: the receive callback doesn't fire when acting as server.
However, `connectToRemoteHost()` works correctly in client mode (send AND receive).

**Solution:** Bitwig connects OUT to our MCP server as a TCP client.

```
┌─────────────────┐     stdio      ┌─────────────────┐    TCP     ┌─────────────────┐
│  Claude Code    │◄──────────────►│                 │◄──────────►│  Bitwig         │
│                 │    MCP         │  Rust MCP       │   :8417    │  Extension      │
└─────────────────┘                │  Server         │            │  (connects out) │
                                   │                 │            └─────────────────┘
┌─────────────────┐   TCP/JSON-RPC │  - Bitwig pool  │
│  Python CLI     │◄──────────────►│  - Tool dispatch│
│  $ bitwig info  │    :8418       │                 │
└─────────────────┘                └─────────────────┘
```

**Components:**
1. **Rust MCP Server** - Listens for Bitwig connections, exposes MCP tools to Claude
2. **Bitwig Extension** - Connects to MCP server on startup, handles commands
3. **Python CLI** - Talks JSON-RPC to MCP server for human use

**Why this design:**
- Bitwig's client-mode TCP works (tested: send AND receive)
- Bitwig's server-mode TCP is broken (send works, receive callback never fires)
- MCP gives Claude Code native tool access
- Single server handles both Claude and CLI clients

### Wire Protocol

All connections use **length-prefixed JSON-RPC 2.0 frames**:

```
┌──────────────────┬─────────────────────────────────┐
│ Length (4 bytes) │ JSON-RPC 2.0 Payload (UTF-8)    │
│ Big-endian u32   │                                 │
└──────────────────┴─────────────────────────────────┘
```

### Ports

| Service | Port | Direction |
|---------|------|-----------|
| MCP Server (Bitwig) | 8417 | Bitwig connects IN |
| MCP Server (CLI) | 8418 | CLI connects IN |

### Legacy: OSC over UDP (retained for real-time)

For real-time control (volume faders, etc.), OSC over UDP may still be used:

| Protocol | Transport | Use Case | Semantics |
|----------|-----------|----------|-----------|
| **JSON-RPC 2.0** | TCP | Commands, queries | Request/response, batching |
| **OSC** | UDP | Real-time control | Fire-and-forget, low latency |

---

## JSON-RPC 2.0 Layer (TCP)

For discrete operations: add tracks, load devices, project management, browser operations.

### Bitwig API Used
```java
// Server setup (in extension init)
RemoteSocket socket = host.createRemoteConnection("BitwigRPC", 8417);
socket.setClientConnectCallback(connection -> {
    connection.setReceiveCallback(data -> handleMessage(connection, data));
    connection.setDisconnectCallback(() -> cleanup(connection));
});

// RemoteConnection methods:
// - send(byte[] data)      Send response
// - setReceiveCallback()   Receive requests
// - disconnect()           Close connection
```

### Known Bitwig API Quirks

**`RemoteSocket.getPort()` returns -1 but socket works** (macOS, Bitwig 5.x)
- The socket IS created and listening (verify with `lsof -i :8417`)
- Connections ARE accepted (callback fires)
- `getPort()` just returns wrong value - ignore it
- Don't treat -1 as failure; test actual connectivity instead

### Wire Protocol: Length-Prefixed Frames

```
┌──────────────────┬─────────────────────────────────┐
│ Length (4 bytes) │ JSON-RPC 2.0 Payload (UTF-8)    │
│ Big-endian u32   │                                 │
└──────────────────┴─────────────────────────────────┘
```

**Example frame (hex):**
```
00 00 00 3D                                    # Length: 61 bytes
7B 22 6A 73 6F 6E 72 70 63 22 3A 22 32 2E ...  # {"jsonrpc":"2.0",...}
```

### JSON-RPC 2.0 Message Format

**Single request:**
```json
{
  "jsonrpc": "2.0",
  "method": "track.create",
  "params": {"type": "instrument", "name": "Bass"},
  "id": 1
}
```

**Single response:**
```json
{
  "jsonrpc": "2.0",
  "result": {"trackId": 0, "name": "Bass"},
  "id": 1
}
```

**Error response:**
```json
{
  "jsonrpc": "2.0",
  "error": {"code": -32602, "message": "Invalid params"},
  "id": 1
}
```

**Batch request (multiple operations in one call):**
```json
[
  {"jsonrpc": "2.0", "method": "track.create", "params": {"type": "instrument"}, "id": 1},
  {"jsonrpc": "2.0", "method": "device.load", "params": {"trackId": 0, "uri": "Polymer"}, "id": 2},
  {"jsonrpc": "2.0", "method": "param.set", "params": {"path": "/track/0/device/0/param/0", "value": 0.5}, "id": 3}
]
```

**Batch response:**
```json
[
  {"jsonrpc": "2.0", "result": {"trackId": 0}, "id": 1},
  {"jsonrpc": "2.0", "result": {"deviceId": 0}, "id": 2},
  {"jsonrpc": "2.0", "result": "ok", "id": 3}
]
```

### RPC Methods (planned)

| Method | Params | Description |
|--------|--------|-------------|
| `track.create` | `{type, name?, index?}` | Create track |
| `track.delete` | `{trackId}` | Delete track |
| `track.rename` | `{trackId, name}` | Rename track |
| `device.load` | `{trackId, uri}` | Load device by URI |
| `device.remove` | `{trackId, deviceId}` | Remove device |
| `browser.search` | `{query, filters?}` | Search browser |
| `browser.load` | `{resultId, trackId?}` | Load browser result |
| `project.save` | `{}` | Save project |
| `project.info` | `{}` | Get project info |
| `clip.create` | `{trackId, sceneId, length}` | Create clip |

### Python Client Example

```python
import socket
import struct
import json

class BitwigRPCClient:
    def __init__(self, host='localhost', port=8417):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self._id = 0

    def _next_id(self):
        self._id += 1
        return self._id

    def _send_frame(self, data: bytes):
        frame = struct.pack('>I', len(data)) + data
        self.sock.sendall(frame)

    def _recv_frame(self) -> bytes:
        length_bytes = self.sock.recv(4)
        length = struct.unpack('>I', length_bytes)[0]
        return self.sock.recv(length)

    def call(self, method: str, params: dict = None):
        """Single RPC call with response."""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self._next_id()
        }
        self._send_frame(json.dumps(request).encode('utf-8'))
        response = json.loads(self._recv_frame().decode('utf-8'))
        if 'error' in response:
            raise Exception(response['error'])
        return response['result']

    def batch(self, calls: list[tuple[str, dict]]):
        """Batch multiple calls, returns list of results."""
        requests = [
            {"jsonrpc": "2.0", "method": m, "params": p or {}, "id": self._next_id()}
            for m, p in calls
        ]
        self._send_frame(json.dumps(requests).encode('utf-8'))
        responses = json.loads(self._recv_frame().decode('utf-8'))
        return [r.get('result') or r.get('error') for r in responses]

# Usage
client = BitwigRPCClient()

# Single call
track = client.call('track.create', {'type': 'instrument', 'name': 'Lead'})

# Batch call - all executed together
results = client.batch([
    ('track.create', {'type': 'instrument'}),
    ('device.load', {'trackId': 0, 'uri': 'Polymer'}),
    ('param.set', {'path': '/track/0/volume', 'value': 0.8}),
])
```

---

## OSC Layer (UDP)

For real-time control: volume, pan, parameters, transport while playing.

### Bitwig API Used
```java
// In extension init
OscModule osc = host.getOscModule();
OscServer server = osc.createUdpServer(8418);
OscAddressSpace addressSpace = server.getAddressSpace();

// Register handlers
addressSpace.registerMethod("/track/*/volume", "*", "Track volume",
    (source, message) -> {
        int trackId = extractTrackId(message.getAddressPattern());
        float value = message.getFloat(0);
        trackBank.getItemAt(trackId).volume().set(value);
    });
```

### OSC Address Space (planned)

| Address | Args | Description |
|---------|------|-------------|
| `/track/{id}/volume` | `f` (0.0-1.0) | Track volume |
| `/track/{id}/pan` | `f` (-1.0 to 1.0) | Track pan |
| `/track/{id}/mute` | `i` (0/1) | Track mute |
| `/track/{id}/solo` | `i` (0/1) | Track solo |
| `/track/{id}/arm` | `i` (0/1) | Track arm |
| `/transport/play` | | Start playback |
| `/transport/stop` | | Stop playback |
| `/transport/tempo` | `f` | Set tempo BPM |
| `/transport/position` | `f` | Set position (beats) |
| `/device/{id}/param/{id}` | `f` (0.0-1.0) | Device parameter |
| `/clip/{track}/{scene}/launch` | | Launch clip |

### Python Client Example

```python
# Using pyliblo3 (actively maintained)
import liblo

# Send OSC messages
target = liblo.Address('localhost', 8418)

# Real-time control
liblo.send(target, '/track/0/volume', 0.75)
liblo.send(target, '/track/0/pan', -0.3)
liblo.send(target, '/transport/tempo', 128.0)
liblo.send(target, '/clip/0/0/launch')
```

---

## Key API Classes by Use Case

| Use Case | JSON-RPC (TCP) | OSC (UDP) |
|----------|----------------|-----------|
| Track management | `TrackBank`, `InsertionPoint` | `Track.volume()`, `Track.pan()` |
| Device control | `Device`, `Browser`, `PopupBrowser` | `Parameter`, `RemoteControlsPage` |
| Transport | `Transport.stop()`, `Transport.record()` | `Transport.tempo()`, `Transport.position()` |
| Clips | `Clip`, `ClipLauncherSlot` | `ClipLauncherSlot.launch()` |
| Project | `Project`, `Application` | - |

---

## Default Ports

| Service | Port | Protocol |
|---------|------|----------|
| JSON-RPC | 8417 | TCP |
| OSC | 8418 | UDP |

---

## Development Philosophy

**No mocks. No fakes. Fail fast and ugly.**

- If Bitwig isn't running, the CLI fails immediately with a clear error
- If the controller extension isn't loaded, you see it right away
- No mock servers, no fake data, no false confidence
- Real errors surface real problems early

**No ripping out code to debug.**

- Add logging, don't remove functionality
- Never restructure code just to isolate a bug
- Keep all features intact while investigating
- Debug by adding `host.println()` statements, not by deleting code
- Never "simplify" code hoping the bug goes away
- Never stab around making random changes
- Add instrumentation to pinpoint and understand the issue first
- Log actual bytes/values in hex when debugging protocol issues

**One CLI, not ad-hoc scripts.**

- All Bitwig operations go through the `bitwig` CLI
- Claude runs `bitwig <command>` via Bash, never writes one-off Python
- New functionality = new CLI command, not a new script
- Keep it simple: `bitwig info`, `bitwig list tracks`, etc.

**Always bump version on rebuild.**

- Increment patch version (0.2.x) on every rebuild
- Update `RPCControllerExtension.VERSION` only (Definition references it)
- User needs to know which version is actually running

**Commit, tag, and push on every working change.**

```bash
# After each working change:
git add -A
git commit -m "descriptive message"
git tag -a v0.2.X -m "Brief description of what works"
git push && git push --tags
```

- Tag format: `v0.2.X` matching the VERSION constant
- Tag message: Brief description of what this version does/fixes
- Push both commits and tags together

---

## Python CLI

### Installation

```bash
# Install in development mode
pip install -e ".[dev]"

# With OSC support
pip install -e ".[dev,osc]"
```

### Usage

```bash
# Show help
bitwig --help

# Show version info (requires Bitwig + controller running)
bitwig info

# List tracks
bitwig list tracks

# With custom host/port
bitwig --host 192.168.1.100 --port 8417 info
```

### Project Structure

```
src/bitwig_cli/
├── __init__.py      # Package version
├── __main__.py      # python -m bitwig_cli entry
├── main.py          # CLI commands (typer)
├── client.py        # JSON-RPC client
├── protocol.py      # Framing + JSON-RPC types
└── config.py        # Configuration
```

### Adding New Commands

1. Add CLI command in `main.py`
2. Implement RPC method in Bitwig extension
3. Test against real Bitwig
