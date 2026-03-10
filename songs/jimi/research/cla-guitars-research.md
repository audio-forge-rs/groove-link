# CLA Guitars Stereo - Research Notes

## Overview

CLA Guitars is a Waves plugin designed by Grammy-winning mixing engineer Chris Lord-Alge. It is an all-in-one multi-effect guitar channel strip, NOT a traditional amp sim. It packages an entire opinionated signal chain into a single interface for fast, professional guitar mixing.

CLA is known for mixing guitar-focused bands: Foo Fighters, Green Day, Muse, My Chemical Romance, Avenged Sevenfold.

## Plugin Architecture

### Input Section (Left)
- **Sensitivity Control**: Ranges from +/- 10 (in 0.1 steps), default 0
  - LED indicator: Green = good, Yellow = optimal, Red = too hot
  - Adjust using the loudest section of the song
- **Guitar Mode**: Clean, Crunch, Heavy
- **Re-Amplify Switch**: Engages a modeled guitar amp tailored to the current mode
  - DI mode: processes already-amped signal (mixing stage)
  - Re-Amp mode: adds amp modeling to DI recordings
  - CPU load increases when Re-Amplify is ON
- **Pan Control**: Input panning

### Effects Section (Middle) - 6 Effect Faders
Each effect has THREE color-coded filter/character presets plus a Clear (bypass) option:

1. **Bass** (Low-frequency EQ)
   - Clear: Bypass
   - Green (Sub): Sub-bass emphasis
   - Blue (Lower): Lower bass frequencies
   - Red (Upper): Upper bass frequencies
   - NOT a standard shelving EQ - these are pre-determined curves CLA would use

2. **Treble** (High-frequency EQ)
   - Clear: Bypass
   - Green (Bite): Bite/presence
   - Blue (Top): Top-end shimmer
   - Red (Roof): Extreme high frequencies
   - Brings pick attack and string noise that helps guitars slice through dense mixes

3. **Compress** (Dynamics)
   - Green (Push): Subtle glue compression
   - Blue (Spank): Aggressive, fast character - "the money-maker" for heavy rhythm guitars
   - Red (Wall): Super-aggressive, brick-wall limiting
   - Evens out palm mutes and open chords

4. **Reverb** (Ambience)
   - Three pre-tuned reverb styles (color-coded)
   - Described as suiting "rock guitars well"
   - Use with caution on tight palm-muted rhythm parts (can cause muddiness)

5. **Delay** (Echo/Repeat)
   - Three preset delay styles including slap-back and Edge-style
   - Can be automated for phrase-ending "throws"
   - Best for leads and ambient textures

6. **Pitch** (Stereo/Chorus/Doubling)
   - Three modes for stereo image expansion
   - Creates subtle widening effects
   - The doubler "doesn't sound flangey" (per KVR user reviews)
   - Very musical chorus-style processing

### Output Section (Right)
- **Output Fader**: Level control
- **Output Meter**: Peak level display

## Signal Chain Order (Internal)

The exact internal signal flow is not fully documented by Waves, but based on manual analysis and the control layout:

```
Input → Sensitivity → [Re-Amp if enabled] → Bass EQ → Treble EQ → Compression → Reverb → Delay → Pitch → Output
```

The signal chain diagram from AudioGeekZine (2010) confirms the CLA signature plugins follow a fixed internal routing that cannot be rearranged.

## Three Guitar Modes

### Clean
- Designed for clean, acoustic, and lightly driven guitar tones
- EQ curves and compression tailored for unprocessed signals
- Re-Amp adds clean amp character

### Crunch
- Mid-gain territory
- Good for rhythm guitars with moderate drive
- Re-Amp adds crunchy amp breakup

### Heavy
- High-gain mode for distorted guitars
- Immediately sets internal EQ curves and compression for distorted guitars
- "Gives your tone a more finished and aggressive character"
- Re-Amp adds heavy amp distortion

## Best Practices for DAW Chain Usage

### As a Standalone Processor
- Works well for demos and pre-production
- Apply to individual guitar tracks or guitar bus
- Presets are "so fully realized they speed up mixing time"

### Combined with Other Effects
- Use AFTER dedicated amp sims (Neural DSP, Fortin, etc.)
- CLA Guitars serves as post-processing/mixing tool
- For surgical EQ work, add a separate parametric EQ before or after
- The plugin is designed for "broad, musical decisions quickly"

### Settings Tips
- **A little goes a long way** - the plugin is calibrated to be sensitive
- **Bass**: Push up if tone is thin, but don't overdo it
- **Heavy mode compression**: Start with "Spank" (Blue) for rhythm guitars
- **Effects on rhythm tracks**: Use reverb/delay sparingly to avoid muddiness
- **Effects on leads**: More reverb/delay/pitch is appropriate

### When NOT to Use
- When you need surgical control (attack/release times, Q settings, specific reverb parameters)
- When you need genre flexibility outside rock/modern rock
- CPU-intensive: ~20% per instance on older systems

## Recreating CLA Guitars Concepts in Bitwig

To emulate the CLA Guitars approach with Bitwig built-in effects:

```
Signal Chain:
1. Amp (for re-amping) → set mode to match Clean/Crunch/Heavy
2. EQ-5 (for Bass/Treble shaping) → low shelf + high shelf
3. Compressor (for dynamics) → adjust for Push/Spank/Wall character
4. Reverb (for ambience) → short decay, rock-appropriate
5. Delay+ (for echo) → slapback or rhythmic delay
6. Micro-Pitch or Chorus (for stereo width/doubling)
```

## Sound Quality Assessment

### Pros (from reviews)
- Fast, professional results
- Excellent for modern rock guitar sounds
- Very musical preset curves
- Good stereo widening without artifacts
- "Nail that modern rock sound that somehow preserves note definition despite being ridiculously distorted"

### Cons (from reviews)
- Limited flexibility for advanced engineers
- Cannot adjust attack/release, Q, or specific reverb parameters
- Genre-specific (primarily rock)
- CPU-intensive
- Better as starting point than complete solution for experienced mixers

## Sources

- Waves Audio official product page
- Nail The Mix: Using CLA Guitars for Aggressive Metal Tones
- Sound on Sound: CLA Artist Signature Collection review
- Stock Music Musician: CLA Guitars review
- KVR Audio product listing and forum discussions
- Waves CLA Guitars User Manual (PDF)
- ElectroSmash Tube Screamer Circuit Analysis (for comparison context)
