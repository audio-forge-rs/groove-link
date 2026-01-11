# Bitwig Control Surface API - Index

This index helps navigate the full API documentation in `bitwig-control-surface-api.md`.
Line numbers are provided for direct navigation.

## Quick Reference - Most Important Classes

### Core Extension Classes
| Class | Line | Description |
|-------|------|-------------|
| Extension | 16 | Base class for all extensions |
| ExtensionDefinition | 223 | Defines extension metadata (name, author, version, UUID) |
| ControllerExtension | 18090 | Base class for controller extensions |
| ControllerExtensionDefinition | 18427 | Defines controller extension metadata |
| ControllerHost | 48259 | Main interface to talk to Bitwig Studio |

### Transport & Playback
| Class | Line | Description |
|-------|------|-------------|
| Transport | 107178 | Control play, stop, record, tempo, time signature |
| Arranger | 29627 | Arranger timeline control |
| Project | 90634 | Project-level settings and state |
| Groove | 68210 | Global groove settings |

### Tracks & Mixing
| Class | Line | Description |
|-------|------|-------------|
| Track | 105679 | Track properties (volume, pan, mute, solo, arm) |
| TrackBank | 105679 | Bank of tracks for navigation |
| CursorTrack | 58932 | Currently selected track |
| MasterTrack | 75366 | Master track control |
| Channel | 39456 | Base channel interface |
| Mixer | 77540 | Mixer panel control |
| Send | 95950 | Send amount control |

### Clips & Scenes
| Class | Line | Description |
|-------|------|-------------|
| Clip | 43828 | Clip properties and content |
| CursorClip | 56047 | Currently selected/edited clip |
| ClipLauncherSlot | 44764 | Launcher slot control |
| ClipLauncherSlotBank | 45737 | Bank of launcher slots |
| Scene | 93811 | Scene triggering |
| SceneBank | 94622 | Bank of scenes |

### Devices & Parameters
| Class | Line | Description |
|-------|------|-------------|
| Device | 63925 | Device control (enable, parameters, presets) |
| DeviceBank | 64710 | Bank of devices |
| CursorDevice | 56834 | Currently selected device |
| Parameter | 86459 | Parameter value control |
| RemoteControl | 92791 | Remote control page parameters |
| RemoteControlsPage | 92968 | Page of remote controls |

### Hardware Abstraction
| Class | Line | Description |
|-------|------|-------------|
| HardwareSurface | 72733 | Define hardware controls |
| HardwareButton | 69632 | Physical button |
| HardwareSlider | 71914 | Physical slider/fader |
| AbsoluteHardwareKnob | 24428 | Absolute knob (0-127) |
| RelativeHardwareKnob | 91943 | Relative/endless encoder |
| HardwareLight | 71021 | LED/light output |
| MultiStateHardwareLight | 79913 | Multi-color LED |

### MIDI I/O
| Class | Line | Description |
|-------|------|-------------|
| MidiIn | 77222 | MIDI input port |
| MidiOut | 77540 | MIDI output port |
| NoteInput | 80662 | Note input for instruments |
| ShortMidiMessage | 13131 | Parse MIDI messages |
| SysexBuilder | 14227 | Build SysEx messages |

### OSC (Open Sound Control)
| Class | Line | Description |
|-------|------|-------------|
| OscModule | 12655 | Get OSC server/client |
| OscServer | 13071 | OSC server |
| OscConnection | 11479 | OSC client connection |
| OscMessage | 12125 | OSC message |
| OscAddressSpace | 11143 | Register OSC method handlers |

### Note/Clip Editing
| Class | Line | Description |
|-------|------|-------------|
| NoteStep | 83862 | Note data in a step |
| NoteOccurrence | 81957 | Note occurrence properties |
| Arpeggiator | 29627 | Arpeggiator control |

### Values & Settings
| Class | Line | Description |
|-------|------|-------------|
| SettableRangedValue | 97984 | Settable 0-1 value |
| SettableBooleanValue | 96565 | Settable boolean |
| SettableStringValue | 98270 | Settable string |
| BooleanValue | 32560 | Observable boolean |
| StringValue | 100827 | Observable string |
| ColorValue | 47762 | Observable color |
| Settings | 99213 | Extension settings |
| Preferences | 88682 | Extension preferences |
| DocumentState | 66165 | Per-project state |

---

## Full Section Index by Package

### Core (lines 8-799)
- Overview: 8
- Extension: 16
- ExtensionDefinition: 223

### com.bitwig.extension.api (lines 800-2737)
- Package summary: 800
- Color: 989
- Host: 1655
- MemoryBlock: 2290
- PlatformType: 2437

### com.bitwig.extension.api.graphics (lines 2738-10590)
- Package summary: 2738
- Bitmap: 3130
- BitmapFormat: 3533
- FontExtents: 3861
- FontFace: 4125
- FontOptions: 4229
- GradientPattern: 4533
- GraphicsOutput: 5955
- GraphicsOutput.AntialiasMode: 4691
- GraphicsOutput.FillRule: 5019
- GraphicsOutput.HintMetrics: 5299
- GraphicsOutput.HintStyle: 5603
- GraphicsOutput.LineCap: 7847
- GraphicsOutput.LineJoin: 8151
- GraphicsOutput.Operator: 8455
- GraphicsOutput.SubPixelOrder: 9383
- Image: 9735
- MeshPattern: 9882
- Path: 10162
- Pattern: 10176
- Renderer: 10193
- TextExtents: 10287

### com.bitwig.extension.api.opensoundcontrol (lines 10591-13070)
- Package summary: 10591
- OscAddressSpace: 10864
- OscBundle: 11143
- OscConnection: 11281
- OscInvalidArgumentTypeException: 11479
- OscIOException: 11635
- OscMessage: 11746
- OscMethod: 12125
- OscMethodCallback: 12309
- OscModule: 12401
- OscNode: 12655
- OscPacket: 12740
- OscPacketSizeExceededException: 12850
- OscServer: 12960

### com.bitwig.extension.api.util.midi (lines 13071-14569)
- Package summary: 13071
- ShortMidiMessage: 13131
- SysexBuilder: 14227

### com.bitwig.extension.callback (lines 14570-17383)
- Package summary: 14570
- BooleanValueChangedCallback: 15004
- Callback: 15099
- ClipLauncherSlotBankPlaybackStateChangedCallback: 15114
- ColorValueChangedCallback: 15227
- ConnectionEstablishedCallback: 15332
- DataReceivedCallback: 15427
- DirectParameterDisplayedValueChangedCallback: 15522
- DirectParameterNameChangedCallback: 15617
- DirectParameterNormalizedValueChangedCallback: 15712
- DoubleValueChangedCallback: 15807
- EnumValueChangedCallback: 15902
- FloatValueChangedCallback: 15931
- IndexedBooleanValueChangedCallback: 16026
- IndexedColorValueChangedCallback: 16124
- IndexedStringValueChangedCallback: 16232
- IndexedValueChangedCallback: 16340
- IntegerValueChangedCallback: 16358
- NoArgsCallback: 16453
- NotePlaybackCallback: 16548
- NoteStepChangedCallback: 16643
- ObjectValueChangedCallback: 16738
- ShortMidiDataReceivedCallback: 16836
- ShortMidiMessageReceivedCallback: 16947
- StepDataChangedCallback: 17105
- StringArrayValueChangedCallback: 17210
- StringValueChangedCallback: 17239
- SysexMidiDataReceivedCallback: 17268
- ValueChangedCallback: 17366

### com.bitwig.extension.controller (lines 17384-20539)
- Package summary: 17384
- AutoDetectionMidiPortNames: 17646
- AutoDetectionMidiPortNamesList: 17838
- ControllerExtension: 18090
- ControllerExtensionDefinition: 18427
- HardwareDeviceMatcher: 18958
- HardwareDeviceMatcherList: 19151
- UsbConfigurationMatcher: 19428
- UsbDeviceMatcher: 19672
- UsbEndpointMatcher: 19957
- UsbInterfaceMatcher: 20207
- UsbMatcher: 20403

### com.bitwig.extension.controller.api (lines 20540-114379)
- Package summary: 20540
- AbsoluteHardwarControlBindable: 23848
- AbsoluteHardwareControl: 24008
- AbsoluteHardwareControlBinding: 24317
- AbsoluteHardwareKnob: 24359
- AbsoluteHardwareValueMatcher: 24428
- Action: 24453
- ActionCategory: 24761
- Application: 24970
- Arpeggiator: 29025
- Arranger: 29627
- AsyncTransferCompledCallback: 30830
- AudioHardwareIoInfo: 30934
- AudioIoDeviceMatcher: 31045
- Bank: 31063
- BeatTimeFormatter: 31472
- BeatTimeValue: 31587
- BitwigBrowsingSession: 31908
- BooleanHardwareProperty: 32129
- BooleanValue: 32399
- Browser: 32560
- BrowserColumn: 33519
- BrowserFilterColumn: 33868
- BrowserFilterColumnBank: 34215
- BrowserFilterItem: 34895
- BrowserFilterItemBank: 35098
- BrowserItem: 35172
- BrowserItemBank: 35479
- BrowserResultsColumn: 36142
- BrowserResultsItem: 36334
- BrowserResultsItemBank: 36387
- BrowsingSession: 36461
- BrowsingSessionBank: 37140
- ChainSelector: 37830
- Channel: 38147
- ChannelBank: 39456
- Clip: 40901
- ClipBrowsingSession: 43828
- ClipLauncherSlot: 43988
- ClipLauncherSlotBank: 44764
- ClipLauncherSlotOrScene: 45737
- ClipLauncherSlotOrSceneBank: 46736
- ColorHardwareProperty: 47202
- ColorValue: 47472
- ContinuousHardwareControl: 47762
- ContinuousHardwareValueMatcher: 48231
- ControllerHost: 48259
- CueMarker: 53760
- CueMarkerBank: 54097
- Cursor: 54253
- CursorBrowserFilterColumn: 54771
- CursorBrowserFilterItem: 54845
- CursorBrowserItem: 55401
- CursorBrowserResultItem: 55560
- CursorBrowsingSession: 55634
- CursorChannel: 55708
- CursorClip: 55891
- CursorDevice: 56047
- CursorDeviceFollowMode: 56834
- CursorDeviceLayer: 57275
- CursorDeviceSlot: 57373
- CursorNavigationMode: 57497
- CursorRemoteControlsPage: 57803
- CursorTrack: 58303
- DeleteableObject: 58932
- DetailEditor: 59088
- Device: 59356
- DeviceBank: 63925
- DeviceBrowsingSession: 64710
- DeviceChain: 64986
- DeviceLayer: 65684
- DeviceLayerBank: 65761
- DeviceMatcher: 65951
- DeviceSlot: 65968
- DirectParameterValueDisplayObserver: 66018
- DocumentState: 66131
- DoubleValue: 66165
- DrumPad: 66331
- DrumPadBank: 66492
- DuplicableObject: 66831
- EnumDefinition: 66982
- EnumValue: 67187
- EnumValueDefinition: 67360
- GenericBrowsingSession: 67645
- Groove: 67867
- HardwareAction: 68210
- HardwareActionBindable: 68451
- HardwareActionBinding: 68607
- HardwareActionMatcher: 68641
- HardwareBindable: 68664
- HardwareBinding: 68684
- HardwareBindingSource: 68794
- HardwareBindingWithRange: 69024
- HardwareBindingWithSensitivity: 69225
- HardwareButton: 69346
- HardwareControl: 69632
- HardwareControlType: 70042
- HardwareDevice: 70343
- HardwareElement: 70453
- HardwareInputMatcher: 70953
- HardwareLight: 70976
- HardwareLightVisualState: 71021
- HardwareOutputElement: 71497
- HardwarePixelDisplay: 71618
- HardwareProperty: 71744
- HardwareSlider: 71764
- HardwareSurface: 71914
- HardwareTextDisplay: 72733
- HardwareTextDisplayLine: 72859
- InputPipe: 73046
- InsertionPoint: 73212
- IntegerHardwareProperty: 73847
- IntegerValue: 74117
- InternalHardwareLightState: 74323
- LastClickedParameter: 74533
- Macro: 74758
- MasterRecorder: 75005
- MasterTrack: 75284
- MidiExpressions: 75366
- MidiIn: 75771
- MidiOut: 77222
- Mixer: 77540
- ModulationSource: 79025
- MultiSampleBrowsingSession: 79455
- MultiStateHardwareLight: 79615
- MusicBrowsingSession: 79913
- NoteInput: 80073
- NoteInput.NoteExpression: 80662
- NoteLatch: 81115
- NoteOccurrence: 81459
- NoteStep: 81957
- NoteStep.State: 83862
- NotificationSettings: 84169
- ObjectArrayValue: 84674
- ObjectHardwareProperty: 84864
- ObjectProxy: 85134
- OnOffHardwareLight: 85298
- OutputPipe: 85626
- Parameter: 85776
- ParameterBank: 86459
- PianoKeyboard: 86669
- PinnableCursor: 86917
- PinnableCursorClip: 87049
- PinnableCursorDevice: 87131
- Pipe: 87229
- PlayingNote: 87252
- PlayingNoteArrayValue: 87383
- PopupBrowser: 87505
- Preferences: 88648
- PresetBrowsingSession: 88682
- PrimaryDevice: 89996
- PrimaryDevice.ChainLocation: 88966
- PrimaryDevice.DeviceType: 89374
- Project: 89674
- RangedValue: 90634
- RelativeHardwarControlBindable: 91109
- RelativeHardwareControl: 91263
- RelativeHardwareControlBinding: 91779
- RelativeHardwareControlToRangedValueBinding: 91824
- RelativeHardwareKnob: 91874
- RelativeHardwareValueMatcher: 91943
- RelativePosition: 91968
- RemoteConnection: 92322
- RemoteControl: 92576
- RemoteControlsPage: 92791
- RemoteSocket: 92968
- SampleBrowsingSession: 93130
- Scene: 93290
- SceneBank: 93811
- Scrollable: 94622
- ScrollbarModel: 95254
- Send: 95665
- SendBank: 95950
- SettableBeatTimeValue: 96011
- SettableBooleanValue: 96281
- SettableColorValue: 96565
- SettableDoubleValue: 96783
- SettableEnumValue: 96967
- SettableIntegerValue: 97107
- SettableRangedValue: 97301
- SettableStringArrayValue: 97984
- SettableStringValue: 98130
- Setting: 98270
- Settings: 98601
- Signal: 99213
- SoloValue: 99369
- SourceSelector: 99571
- SpecificBitwigDevice: 99874
- SpecificDevice: 100021
- SpecificPluginDevice: 100063
- StringArrayValue: 100170
- StringHardwareProperty: 100314
- StringValue: 100654
- Subscribable: 100827
- TimelineEditor: 101074
- TimeSignatureValue: 101662
- Track: 102165
- TrackBank: 105679
- Transport: 107178
- UsbDevice: 112361
- UsbInputPipe: 112554
- UsbInterface: 112591
- UsbOutputPipe: 112793
- UsbPipe: 112830
- UsbTransferDirection: 113109
- UsbTransferStatus: 113416
- UsbTransferType: 113818
- UserControlBank: 114095
- Value: 114211

---

## Common Patterns

### Getting Started
1. Extend `ControllerExtension` (line 18090)
2. Define metadata in `ControllerExtensionDefinition` (line 18427)
3. In `init()`, get `ControllerHost` to access Bitwig APIs

### Critical: init() Constraints (line 18381)
**ALL `host.create*()` methods MUST be called during `init()`**

```java
@Override
public void init() {
    // ALL create* calls MUST happen here
    transport = host.createTransport();
    trackBank = host.createTrackBank(8, 0, 0);
    rpcSocket = host.createRemoteConnection("RPC", 8417);  // TCP server
    // etc.
}
```

If called from `scheduleTask()` or elsewhere: `Exception: Trying to create section outside of init()`

**Includes:** createRemoteConnection, createTrackBank, createTransport, createApplication, createNoteInput (line 76563), all other create* methods.

### Service Discovery
Extension JAR must contain:
```
META-INF/services/com.bitwig.extension.ExtensionDefinition
```
Contents: fully qualified class name of your ExtensionDefinition

**Wrong:** `com.bitwig.extension.controller.ControllerExtensionDefinition` (won't be discovered)

### Accessing Bitwig State
```
ControllerHost host = getHost();
Transport transport = host.createTransport();
TrackBank trackBank = host.createTrackBank(8, 0, 0);
CursorTrack cursorTrack = host.createCursorTrack(0, 0);
```

### Observing Values
All `Value` types support `.addValueObserver(callback)` to react to changes.
Call `.markInterested()` on values you want to observe.

### Hardware Binding
1. Create `HardwareSurface`
2. Define hardware elements (buttons, knobs, sliders)
3. Bind to Bitwig parameters or actions

### Network I/O (lines 52383-52468, 92968-93119)
| Method | Description |
|--------|-------------|
| `createRemoteConnection(name, port)` | TCP server socket (line 52383) |
| `connectToRemoteHost(host, port, cb)` | TCP client connection (line 52412) |
| `sendDatagramPacket(host, port, data)` | UDP send (line 52440) |
| `addDatagramPacketObserver(...)` | UDP receive (line 52468) |

`RemoteSocket.getPort()` returns actual port (-1 if failed, may differ from requested if busy)
