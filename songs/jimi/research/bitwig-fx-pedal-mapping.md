# Bitwig Built-in FX to Guitar Pedal Mapping

## Standard Guitar Pedal Signal Chain Order

The universally recommended order for guitar pedals:

```
Guitar → Tuner → Compressor → Wah/Filter → Overdrive → Distortion → Fuzz
       → EQ → Modulation (Chorus/Phaser/Flanger) → Tremolo → Delay → Reverb → Amp
```

Effects loop (between preamp and power amp):
```
Preamp → Modulation → Delay → Reverb → Power Amp
```

### Why Order Matters
- Gain-based effects amplify everything before them (including noise)
- Modulation effects work best on already-colored tone
- Time-based effects maintain clarity when applied last
- Compression before drive evens dynamics; after drive tames peaks

---

## Bitwig Device Mapping by Pedal Category

### 1. DYNAMICS / COMPRESSION

**Guitar Pedal**: Compressor (Keeley, Dyna Comp, Ross)
**Bitwig Device**: **Compressor** or **Compressor+**

| Pedal Control | Bitwig Equivalent |
|--------------|-------------------|
| Sustain/Ratio | Ratio parameter |
| Level | Makeup Gain |
| Attack | Attack |
| Tone | Use EQ-5 after compressor |

**Compressor+** features:
- Six compression characters: Smooth, Glue, Smash, and more
- Four frequency bands for multiband analysis
- Standard, Beyond (extended range), and Dual (upward compression) modes
- **For guitar**: "Glue" character works well for evening out dynamics

**Tip**: Compressor+ "Smash" character = aggressive like a heavy stomp compressor

---

### 2. WAH / FILTER

**Guitar Pedal**: Wah (Cry Baby, Vox), Envelope Filter (Mutron III)
**Bitwig Devices**: **Filter+**, **Filter**, **Ladder**, **Sweep**

| Pedal Type | Bitwig Device | Setup |
|-----------|---------------|-------|
| Wah pedal | Filter+ or Ladder | Bandpass mode, modulate cutoff with expression/LFO |
| Auto-wah | Ladder | Use built-in envelope follower to modulate frequency |
| Envelope filter | Filter+ | Use audio modulation source for cutoff |
| Synth filter | Sweep | Waveshaper + dual filters with frequency sweep |

**Filter+** features:
- 10 filter types: Low-pass LD, Sallen-Key, SVF, Comb, Low-pass MG, XP, Vowels, Fizz, Rasp, Ripple
- 14 waveshapers built in
- Signal flow: audio input → waveshaper → filter
- Built-in stereo LFO and audio modulation
- Pre/Post FX chains

**Ladder** features:
- Classic multimode ladder filter
- Built-in LFO, envelope, and envelope follower
- Perfect for auto-wah when envelope follower modulates frequency

---

### 3. OVERDRIVE (Tube Screamer, Klon, Blues Driver)

**Bitwig Approach**: **Saturator** + **EQ-5** (before and/or after)

#### Tube Screamer Emulation Recipe

The Tube Screamer's signature sound comes from:
1. **Mid-hump EQ** centered around 720 Hz
2. **Soft, symmetric clipping** (two diodes in feedback loop)
3. **Frequency-selective distortion** (bass gets less distortion)
4. **Signal preservation** (dry signal mixed with clipped version)

```
Bitwig Chain:
EQ-5 (pre) → Saturator → EQ-5 (post)
```

**Pre-EQ (EQ-5)**:
- High-pass at ~200-300 Hz to cut low-end before saturation
- Gentle mid boost around 700-1000 Hz

**Saturator settings**:
- Drive: moderate (this is soft clipping, not hard)
- Works in log domain "just like our ears"
- Use the curve editor: set Threshold moderate, Amount moderate
- Normalize: ON to maintain level
- The Saturator's log-domain processing naturally creates soft clipping similar to tube circuits

**Post-EQ (EQ-5)**:
- Low-pass around 3-5 kHz to tame harshness
- Additional mid presence boost if needed

**Key**: The Saturator has Skew controls that treat positive and negative transients differently, adding richness - use for asymmetric clipping (even harmonics, more "tube-like")

#### Klon-style Transparent Overdrive
- Saturator with very low Drive
- Mix control blended ~50% (preserves dynamics)
- Minimal EQ shaping - goal is "transparent" gain

#### Blues Driver Style
- Saturator with moderate Drive
- More aggressive high-pass pre-filter
- Wider frequency range than Tube Screamer

---

### 4. DISTORTION (DS-1, RAT, Big Muff)

**Bitwig Device**: **Distortion** or **Amp**

**Distortion** device:
- Based on hard clipping
- Peak EQ before clipping is applied
- High-pass and low-pass filters after clipping
- "Great for smashing stuff, but for more subtle usage it's pretty harsh"

**Amp** device (better for guitar distortion):
- Pre-drive EQ: Low/Mid/High bands
- Drive stage: up to 48 dB gain
- Selectable clipping models: Class AB, Eulic, Fold B, etc.
- Bias and Sag controls (amp-like behavior)
- Post-drive EQ
- Cabinet simulation with 8 modes, size/color controls
- "Surprisingly has very little aliasing with even some extreme settings"

| Pedal Type | Bitwig Setup |
|-----------|-------------|
| DS-1 | Distortion: moderate drive, mid-scoop post-EQ |
| RAT | Distortion: high drive, low-pass filter engaged |
| Big Muff | Amp with high drive + scooped mid EQ |
| Metal Zone | Distortion maxed + EQ-5 with parametric mid control |

---

### 5. FUZZ (Fuzz Face, Big Muff, Octavia)

**Bitwig Approach**: **Amp** (high drive) or **Bit-8** + **Distortion**

Fuzz characteristics to recreate:
- Extreme clipping (nearly square wave)
- Rich harmonic content
- Often asymmetric clipping
- Sputtery, gated character (for some types)

```
Fuzz Face: Amp with max Drive, low Bias (for sputtery response), cabinet OFF
Big Muff:  Amp with high Drive + EQ-5 (scoop mids around 400-800 Hz)
Octavia:   Pitch Shifter (+12 semitones, 50% mix) → Amp (high drive)
```

**Bit-8** for lo-fi fuzz:
- Clock manipulation for sample-rate reduction
- Quantize for bit-crushing
- Shape with drive and distortion options
- Good for Velvet Fuzz / gated fuzz textures

**Over** (anti-aliased clipper):
- Threshold control
- Multiband blend with Tilt
- Knee control
- Better for clean hard-clipping fuzz without aliasing artifacts

---

### 6. EQ PEDALS (Graphic EQ, Parametric EQ, Mid-Boost)

**Bitwig Device**: **EQ-5**

- 5-band parametric EQ
- Global gain control (adjusts all bands)
- Shift control (moves all band frequencies)
- Frequency visualization

| Pedal | EQ-5 Setup |
|-------|-----------|
| MXR 10-band EQ | Use all 5 bands across spectrum |
| Mid-boost (like TS) | Bell curve at 700-1000 Hz, +6-10 dB |
| Treble booster | High shelf boost at 2-4 kHz |

---

### 7. CHORUS

**Guitar Pedal**: Boss CE-2, Small Clone, Julia
**Bitwig Devices**: **Chorus+** or **Chorus**

**Chorus+** characters:
- **CE**: Synth-style, different tone inspirations (Tone + Width) - closest to CE-2
- **DD**: Subtle, 80s character (Time + Balance) - closest to dimension chorus
- **8v**: Eight voices with feedback caverns (FB + Width) - lush ensemble
- **x2**: Classic voice doubling circuit (Time + Width) - doubler effect

**Chorus** (basic):
- Adjustable LFO with phase offset for right channel (R Phase)
- Simple and effective

| Pedal Style | Chorus+ Character |
|------------|------------------|
| Boss CE-2 | CE mode, moderate depth |
| EHX Small Clone | CE mode, deeper setting |
| Dimension chorus | DD mode |
| Ensemble/12-string | 8v mode |
| Doubler (CLA-style) | x2 mode |

---

### 8. PHASER

**Guitar Pedal**: MXR Phase 90, Small Stone, Boss PH-3
**Bitwig Devices**: **Phaser+** or **Phaser**

**Phaser+** characters:
- **GS**: "Spikey #1 friend" - classic phase sound
- **EHx**: "Classy and smooth, with silky motion" - Small Stone style
- **MX**: "Raspy devil, but solid" - MXR style
- **MF**: "Pleasantly greasy and deep" - deep phase

Modulation curves: Phaser (traditional), Speaking (vowel-like), Barber up, Barber down

**Phaser** (basic):
- 2 to 32 pole allpass filter
- Separate L/R phase controls
- Feedback control
- Modulate with LFO or any of Bitwig's 38 modulator devices

---

### 9. FLANGER

**Guitar Pedal**: Boss BF-2/3, MXR Flanger, Electric Mistress
**Bitwig Devices**: **Flanger+** or **Flanger**

**Flanger+** characters:
- **DP**: "Digital, scrapy cousin who chews up sound"
- **MX**: "Firm, pedal-style classic" - most like traditional flangers
- **TFX**: "Smooth and sparkly, with some edge"
- **WA**: "Stronger, but subtly delicate"

Features:
- Alternate Character toggle
- Stereo-ize option (inverts right modulation)
- Manual Override mode (disable LFOs for custom modulation)
- Added Dirt option for extra coloring

**Flanger** (basic):
- Adjustable LFO
- Feedback magnitude and phase (negative feedback)
- Retrigger on note messages

---

### 10. TREMOLO

**Guitar Pedal**: Boss TR-2, Fender amp tremolo, Supa-Trem
**Bitwig Device**: **Tremolo**

- Multi-shape amplitude modulation
- Various waveshapes (sine, square, triangle, etc.)
- Retrigger on note events
- Rate: 0.010 Hz to 31.623 Hz
- For surf/vintage: sine wave, moderate speed
- For choppy/stutter: square wave, faster speed
- For psychedelic: triangle wave, slow speed

---

### 11. RING MODULATOR

**Guitar Pedal**: Ring Mod (Moog MF-102, EHX Ring Thing)
**Bitwig Devices**: **Ring-Mod** or **Treemonster**

**Ring-Mod**:
- Definable frequency for the carrier oscillator
- Mix control for blending source with sum/difference tones
- Pre- and post-processing device chains
- Classic metallic, bell-like tones

**Treemonster**:
- "Organic zero-crossing amplitude controlled ring modulator with a life of its own"
- Uses incoming audio pitch to tune the ring mod's sine wave
- Pitch detection with threshold control
- Pitch offset for shifting
- Speed slew for response time
- More musical/tracking than standard ring mod
- Great for synth-like guitar textures

---

### 12. DELAY

**Guitar Pedal**: Boss DD series, Carbon Copy, El Capistan, Timeline
**Bitwig Devices**: **Delay+**, **Delay-1**, **Delay-2**, **Delay-4**

| Pedal Style | Bitwig Device | Setup |
|------------|---------------|-------|
| Simple slapback | Delay-1 | 80-120ms, low feedback, no sync |
| Stereo delay | Delay-2 | Different L/R times, crossfeed for movement |
| Dotted-8th (Edge) | Delay+ | Tempo-sync dotted 8th, moderate feedback |
| Multi-tap | Delay-4 | 4 independent taps with separate timing |
| Analog warmth | Delay+ | Engage low-pass in feedback, use Blur "Soft" |
| Tape echo | Delay+ | Repitch mode for wow/flutter, feedback filtering |
| Reverse delay | Delay+ | Blur character "Reverse" |
| Ambient/pad | Delay+ | Long time, high feedback, Blur "Space" or "Wide" |
| Self-oscillation | Delay+ | Feedback > 100% (up to 122%) |

**Delay+ special features**:
- Pattern modes: Mono, Stereo, Ping L, Ping R
- Blur characters: No Blur, Soft, Wide, Still, Space, Reverse
- Ducking envelope follower
- Forever mode (freeze buffer at unity gain)
- FB FX chain for inserting devices in feedback loop
- Detune with stereo inversion for width
- Level control with Soft Clip, Hard Clip, or Comp modes

---

### 13. REVERB

**Guitar Pedal**: Boss RV-6, Hall of Fame, BigSky, Spring reverb
**Bitwig Device**: **Reverb**

- Algorithmic reverb with EARLY reflections and TANK (late reflections)
- Room/Hall modes
- Three assignable frequency bands in tank
- Diffusion/Blur with 6 characters:
  - No Blur, Soft, Wide, Still, Space, Reverse
- Pre-delay control
- Tank FX chain (insert devices into feedback loop!)
- Wet FX chain
- "Surprisingly effective" per reviews

| Reverb Style | Setup |
|-------------|-------|
| Spring | Short decay, high diffusion, Room mode |
| Room | Medium decay, Room mode, moderate wet |
| Hall | Long decay, Hall mode |
| Plate | Medium decay, high diffusion, minimal early reflections |
| Shimmer | Insert Pitch Shifter in Tank FX chain (+12 semi) |
| Ambient/pad | Long decay, Space blur, high wet mix |

---

### 14. PITCH EFFECTS

**Guitar Pedal**: Whammy, POG, Octaver
**Bitwig Devices**: **Pitch Shifter**, **Freq Shifter**, **Freq Shifter+**

**Pitch Shifter**:
- Shift up to ±12 semitones
- Grain control for processing quality
- Mix control for harmonization
- Use for octave-up (Hendrix), octave-down, harmony

**Freq Shifter / Freq Shifter+**:
- Adjustable frequency shift (not pitch - creates inharmonic content)
- Stereo distribution of up/down shifts
- Optional delay network (Freq Shifter+)
- Feedback with filtering
- Good for through-zero flanging and metallic textures

---

### 15. COMB FILTER

**Guitar Pedal**: No direct equivalent (found in some synth pedals)
**Bitwig Device**: **Comb** (under Filter category)

- Bipolar feedback controls
- Two comb filters per stereo channel
- Mix control
- Creates resonant, metallic, pitched filtering
- Use for: resonant effects, pseudo-reverb, metallic textures

**Blur** (under Audio FX):
- Comb-filter diffusion effect
- Each stereo channel has two comb filters with two feedback controls
- More diffusion-oriented than the Comb device

---

### 16. BIT CRUSHER / LO-FI

**Guitar Pedal**: Bit Commander, Data Corruptor, lo-fi pedals
**Bitwig Device**: **Bit-8**

- Clock manipulation (sample rate reduction)
- Amplitude gate
- Shape with drive and various distortion options
- Quantize modes (bit depth reduction)
- Anti-alias option
- Stereo Width control
- Wet FX chain

---

### 17. ROTARY SPEAKER

**Guitar Pedal**: Rotary sim (Strymon Lex, EHX Lester)
**Bitwig Device**: **Rotary**

- Rotary-speaker emulation
- Modulates signal placement in stereo field
- Classic Leslie cabinet effect for guitars

---

### 18. UTILITY / TOOL

**Bitwig Device**: **Tool**

- Volume, Pan, Phase controls
- Stereo width
- DC offset correction
- Useful for gain staging between effects
- Essential for level-matching in complex chains

---

## Complete Pedal Board Emulation Chain in Bitwig

```
Guitar Input
  → Compressor+ (dynamics evening)
  → Ladder (wah/envelope filter - with expression control)
  → EQ-5 (pre-gain EQ / mid boost)
  → Saturator (overdrive / tube screamer)
  → Distortion or Amp (distortion / fuzz)
  → EQ-5 (post-gain tone shaping)
  → Chorus+ / Phaser+ / Flanger+ (modulation)
  → Tremolo (amplitude modulation)
  → Delay+ (echo/repeat)
  → Reverb (ambience)
  → Tool (output level / gain staging)
```

## Gain Stacking in Bitwig

To emulate stacking multiple overdrive/distortion pedals:

```
EQ-5 (mid boost) → Saturator (light OD) → Saturator (heavier OD) → Amp (amp breakup)
```

Each gain stage adds harmonics and compression. The order matters:
- Light OD → Heavy OD = tighter, more focused
- Heavy OD → Light OD = looser, more compressed

## Key Bitwig Advantages for Guitar FX

1. **Modulation system**: Any parameter can be modulated by 38+ modulator types
2. **FX chains within devices**: Reverb tank FX, Delay feedback FX, Filter pre/post FX
3. **Nested containers**: FX Layer for parallel processing, Chain for serial
4. **Per-voice processing**: Poly effects possible with voice stacking
5. **Macro controls**: Map multiple parameters to single knobs

## Sources

- BOSS: Ultimate Guide to Guitar Effects Pedal Order
- JHS Pedals: How to Order Your Pedals
- Bitwig User Guide: destruction, modulation_fx, delay, filter, audio_fx, reverb sections
- AdmiralBumbleBee: Bitwig Effects Review
- Bitwig.com: Learnings series (Amp, Chorus+, Flanger+, Phaser+, Micro-Pitch)
- Polarity.me: Saturator guide, Delay-1 guide, Pitch Shifter guide
- ElectroSmash: Tube Screamer Circuit Analysis
- SonicScoop: Getting That Tube Screamer Sound
- Perfect Circuit: Overdrive vs Distortion vs Fuzz
- anasounds.com: OD/Disto/Fuzz differences
