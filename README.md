# Groove Link

Control Bitwig Studio from Claude Code or the command line.

```
┌─────────────────┐                ┌─────────────────┐    TCP     ┌─────────────────┐
│  Claude Code    │──── Bash ─────►│  Python CLI     │◄──────────►│  Rust TCP       │
│                 │                │  $ bitwig ...   │   :8418    │  Proxy          │
└─────────────────┘                └─────────────────┘            │                 │
                                                                  │                 │
                                                                  │            :8417│
                                                                  └────────▲────────┘
                                                                           │
                                                                  ┌────────┴────────┐
                                                                  │  Bitwig         │
                                                                  │  Extension      │
                                                                  │  (connects out) │
                                                                  └─────────────────┘
```

## Quick Start

### 1. Build the TCP Proxy (Rust)

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
# Start the TCP proxy
./mcp-server/target/release/groove_link &

# Open Bitwig Studio (extension auto-connects)
# Then:
bitwig info
bitwig list tracks
```

## Claude Code Integration

Claude Code uses the Python CLI via Bash. No MCP server registration needed.

```
Claude: "Create an instrument track with Polymer"
→ runs: bitwig project create config.yaml
```

The CLI has all the domain knowledge: device resolution, search, track creation.

## CLI Commands

```bash
bitwig info                       # Show version info
bitwig list tracks                # List all tracks
bitwig preset <query>             # Search Bitwig presets
bitwig project create song.yaml     # Create tracks from YAML config
bitwig --help                     # Show all commands
```

### Search Commands

Fast fuzzy search across all installed content:

```bash
# Bitwig presets
bitwig preset reverb                # Search for reverb presets
bitwig preset delay --type fx       # Filter audio effects only
bitwig preset arp -t note           # Filter note effects only

# Bitwig base devices (core devices, not presets)
bitwig device receiver              # Find Audio Receiver, Note Receiver
bitwig device compressor            # Find Compressor, Compressor+
bitwig device delay -c fx           # Filter to audio effects only

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

**Device category filters:**
- `inst` - Instruments (Polymer, Drum Machine)
- `note` - Note effects (Note Receiver, Arpeggiator)
- `fx` - Audio effects (Compressor, Delay+)
- `routing` - Routing devices (Audio Receiver, Note Receiver)
- `mod` - Modulators (LFO, ADSR)
- `util` - Utilities (Test Tone, DC Offset)

### Project Setup

Create complete project setups from a declarative YAML config:

```bash
bitwig project create song.yaml              # Create all tracks
bitwig project create song.yaml --track piano  # Create specific track
```

**Song config format (see `examples/morning-light.yaml`):**

```yaml
song:
  title: Morning Light
  tempo: 72

tracks:
  piano:
    instrument: nektar piano
    note_fx:
      - Humanize x 3           # Natural timing variation
    fx:
      - Smooth Compression     # Dynamics control
      - Tape-Machine           # Warm character
    part: morning-light-piano.abc

  bass:
    instrument: Acoustic Bass Long
    fx:
      - Analogue Compressor
    part: morning-light-bass.abc

  pad:
    instrument: Ambient Strings
    note_fx:
      - 8th Note Delay         # Rhythmic echoes
      - Humanize x 3
    fx:
      - Handmade Chorus        # Stereo width
      - Smooth Compression
      - Ducking Soft Stereo Feed

  room:                        # Shared FX track
    receives:
      - piano: pre
      - bass: pre
      - pad: pre
    fx:
      - Room One
      - EQ-5

  master:                      # Mastering chain
    fx:
      - EQ-5
      - Focused Mastering
      - Peak Limiter
```

**Features:**
- Declarative format: `instrument`, `note_fx`, `fx`, `part`, `receives`
- Devices fuzzy-matched against presets, base devices, and plugins
- `receives` creates Audio Receiver devices for shared FX routing
- `master` track adds effects to the master bus
- ABC notation auto-converted to MIDI via `abc2midi`

## How It Works

1. **Rust TCP Proxy** listens on port 8417 (Bitwig) and 8418 (CLI)
2. **Bitwig Extension** connects OUT to proxy as TCP client
3. **Python CLI** sends JSON-RPC requests to proxy
4. **Claude Code** runs CLI commands via Bash

Why this architecture? Bitwig's server-mode TCP receive callback is broken. Client mode works.

## Project Structure

```
groove-link/
├── mcp-server/          # Rust TCP proxy (misnamed, no MCP)
│   └── src/
│       ├── main.rs      # Entry point
│       ├── server.rs    # CLI connection handler
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
│   ├── abc.py           # ABC notation to MIDI conversion
│   ├── resolve.py       # Device name resolution
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
