# Groove Link

Control Bitwig Studio from Claude Code or the command line.

```
┌─────────────────┐     stdio      ┌─────────────────┐    TCP     ┌─────────────────┐
│  Claude Code    │◄──────────────►│                 │◄──────────►│  Bitwig         │
│                 │    MCP         │  Rust MCP       │   :8417    │  Extension      │
└─────────────────┘                │  Server         │            │  (connects out) │
                                   │                 │            └─────────────────┘
┌─────────────────┐   TCP/JSON-RPC │                 │
│  Python CLI     │◄──────────────►│                 │
│  $ bitwig info  │    :8418       │                 │
└─────────────────┘                └─────────────────┘
```

## Quick Start

### 1. Build the MCP Server (Rust)

```bash
cd mcp-server
cargo build --release
```

### 2. Build the Bitwig Extension (Java)

```bash
cd controller
mvn package
cp target/RPCController.bwextension ~/Documents/Bitwig\ Studio/Extensions/
```

### 3. Install the Python CLI

```bash
pip install -e ".[dev]"
```

### 4. Start Everything

```bash
# Start the MCP server
./mcp-server/target/release/groove_mcp &

# Open Bitwig Studio (extension auto-connects)
# Then:
bitwig info
bitwig list tracks
```

## Claude Code Integration

Register the MCP server with Claude Code:

```bash
claude mcp add groove-link /path/to/groove-link/mcp-server/target/release/groove_mcp -- --stdio
```

Restart Claude Code. Now Claude has direct access to Bitwig tools:

| Tool | Description |
|------|-------------|
| `bitwig_info` | Get Bitwig/controller version info |
| `bitwig_list_tracks` | List all tracks in the project |
| `bitwig_status` | Check if Bitwig is connected |

**Startup order matters:** Start Claude Code first (spawns MCP server), then start/reload Bitwig.

## CLI Commands

```bash
bitwig info                       # Show version info
bitwig list tracks                # List all tracks
bitwig preset <query>             # Search Bitwig presets
bitwig track create song.yaml     # Create tracks from YAML config
bitwig --help                     # Show all commands
```

### Search Commands

Fast fuzzy search across all installed content:

```bash
# Bitwig presets
bitwig preset reverb                # Search for reverb presets
bitwig preset delay --type fx       # Filter audio effects only
bitwig preset arp -t note           # Filter note effects only

# Audio plugins (VST3, AU, CLAP)
bitwig plugin kontakt               # Find Kontakt plugins
bitwig plugin surge --format clap   # Filter by format

# Kontakt instruments
bitwig kontakt piano                # Search Kontakt library
bitwig kontakt bass -l "Session"    # Filter by library

# M-Tron Pro IV patches
bitwig mtron violins                # Search M-Tron patches
bitwig mtron choir --category Voices # Filter by category
```

**Preset type filters:**
- `inst` - Instruments (Polymer, Phase-4, Sampler)
- `note` - Note effects (Note Delay, Arpeggiator)
- `fx` - Audio effects (Delay+, Reverb, Compressor)

### Track Creation

Create tracks with device chains from a YAML config:

```bash
bitwig track create song.yaml              # Create all tracks
bitwig track create song.yaml --track piano  # Create specific track
```

**Song config format:**

```yaml
name: My Song

tracks:
  piano:
    type: instrument
    devices:
      - Humanize x 3        # Note FX preset
      - nektar piano        # Instrument preset
      - dynamic eq          # Effect preset
      - Multiband Dynamics  # Effect preset (Abbey Road style)
      - reverb              # Effect preset
```

Devices are resolved via fuzzy search - use exact names or partial matches.

## How It Works

1. **Rust MCP Server** listens on port 8417 (Bitwig) and 8418 (CLI)
2. **Bitwig Extension** connects OUT to MCP server as TCP client
3. **Python CLI** sends JSON-RPC requests to MCP server
4. **Claude Code** talks MCP over stdio to the server

Why this architecture? Bitwig's server-mode TCP receive callback is broken. Client mode works.

## Project Structure

```
groove-link/
├── mcp-server/          # Rust MCP server
│   └── src/
│       ├── main.rs      # Entry point
│       ├── server.rs    # MCP tools + CLI handler
│       ├── bitwig.rs    # Bitwig connection manager
│       └── protocol.rs  # Length-prefixed JSON-RPC framing
├── controller/          # Java Bitwig extension
│   └── src/main/java/com/bitwig/extensions/rpc/
│       ├── RPCControllerExtension.java
│       └── RPCControllerExtensionDefinition.java
├── src/bitwig_cli/      # Python CLI
│   ├── main.py          # CLI commands
│   ├── client.py        # JSON-RPC client
│   ├── protocol.py      # Framing
│   ├── presets.py       # Preset search (Spotlight-based)
│   └── table.py         # Adaptive table display
├── docs/                # Documentation
│   └── CLI_SEARCH_SPEC.md  # Search commands spec
└── CLAUDE.md            # Detailed docs for Claude Code
```

## Wire Protocol

All TCP connections use length-prefixed JSON-RPC 2.0:

```
┌──────────────────┬─────────────────────────────────┐
│ Length (4 bytes) │ JSON-RPC 2.0 Payload (UTF-8)    │
│ Big-endian u32   │                                 │
└──────────────────┴─────────────────────────────────┘
```

## License

MIT
