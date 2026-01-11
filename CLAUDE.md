# CLAUDE.md

## Project Overview

This project is a Bitwig Studio controller extension that exposes Bitwig's functionality via REST and/or OSC interfaces.

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

### OSC Integration
The Bitwig API includes built-in OSC support via `OscModule`:
- Create OSC servers to receive messages
- Create OSC connections to send messages
- Register method handlers for incoming OSC addresses
