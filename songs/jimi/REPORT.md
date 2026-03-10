# Jimi — Track Report

**Tempo:** 92 BPM | **Key:** E minor | **Time:** 4/4 | **Length:** ~8 minutes (184 bars)

## Concept

Two guitar parts (A and B) split across 8 tracks, each demonstrating a unique pedal technique from JHS Pedals episodes. Every track runs through a Kontakt 8 guitar (Electric Sunburst Deluxe Melody), Bitwig native FX emulating specific pedal chains, and a CLA Guitars Stereo instance as the amp simulator.

Parts A and B shift independently across their four tracks — sometimes a single track carries the part for bars at a time, sometimes the part fragments across 2-3 tracks with overlap. The cuts between Part A's four tracks are NOT synced to Part B's cuts.

---

## Reference Tracks

### part-a-ref
- **Role:** Full Part A composition (lead/melody dominant)
- **FX:** None — raw Kontakt instrument only
- **Purpose:** Compositional reference, not for playback

### part-b-ref
- **Role:** Full Part B composition (rhythm/countermelody dominant)
- **FX:** None — raw Kontakt instrument only
- **Purpose:** Compositional reference, not for playback

---

## Part A Tracks (Lead/Melody)

### A1: Transparent Stack
- **JHS Source:** Stack episode — "Morning Glory + Klon Centaur"
- **Concept:** Blues breaker transparent OD (always-on first stage, no mid peak) into Klon-style mid-heavy OD (drive cranked to 75%, hard clipping with heavy mid boost)
- **FX Chain:**
  1. Saturator (gentle saturation = transparent blues breaker OD)
  2. EQ-5 (flat with slight presence = "transparent" character)
  3. **CLA Guitars Stereo** (Crunch mode)
  4. Distortion (hard clipping = Klon's diode stage)
  5. EQ-5 (1kHz mid boost = Klon's distinctive EQ)
  6. Compressor (glue)
- **Bars:** Primarily 1-48, 141-160 (melodic foundation sections)
- **JHS Quote:** *"Take a light gain transparent overdrive that you never turn off, then stack a Klon with the drive cranked to 75%. Rich, thick, works on any pickup."*

### A2: Octave Fuzz
- **JHS Source:** Stack episode — "Micro POG into Fuzz War"
- **Concept:** Sub-octave pedal (50% dry, 75% sub, touch of high octave) into massive fuzz. "The loudest, most rambunctious combination."
- **FX Chain:**
  1. Pitch Shifter (-12 semitones = sub octave, mixed with dry)
  2. **CLA Guitars Stereo** (Heavy mode, gain cranked)
  3. Distortion (full fuzz destruction)
  4. Bit-8 (adds gritty texture like analog fuzz harmonics)
  5. EQ-5 (slight mid scoop for Big Muff character)
- **Bars:** Primarily 73-88, 105-120 (heavy/aggressive sections)
- **JHS Quote:** *"Take an octave pedal before a fuzz, set the octave up with 50% dry, 75% sub, a little high octave... it'll frustrate your neighbors and make everyone hate you."*

### A3: Edge Delays
- **JHS Source:** Stack episode — "The Edge of U2" dual delay technique
- **Concept:** Analog delay (quarter notes) into digital delay (dotted eighths). The delays syncopate against each other: "dadada dadada" rhythmic pattern. Clean tone essential for delay clarity.
- **FX Chain:**
  1. EQ-5 (bright, chimey top end for clean sparkle)
  2. **CLA Guitars Stereo** (Clean mode, minimal coloring)
  3. Delay-2 (quarter note delay, analog warmth)
  4. Delay-4 (dotted eighth delay, digital precision)
  5. Reverb (subtle shimmer verb tail)
- **Bars:** Primarily 33-48, 89-104 (atmospheric, chiming sections)
- **JHS Quote:** *"Analog delay as quarter notes, digital delay as dotted eighths. When you tap tempo, both sync. Quarter into dotted eighths — really, really awesome."*

### A4: Nirvana Grunge
- **JHS Source:** Stack + Nirvana episodes — Big Muff into Tube Screamer + Small Clone
- **Concept:** Big Muff's scooped-mid fuzz disappears in a band mix. Fix by running it into a Tube Screamer (mid boost, low drive, high volume) to recover the mids. Add Small Clone chorus for Kurt's signature texture.
- **FX Chain:**
  1. Distortion (heavy fuzz = Big Muff)
  2. EQ-5 (scoop mids = Big Muff's natural character)
  3. **CLA Guitars Stereo** (Heavy mode)
  4. Saturator (soft clipping OD = Tube Screamer mid recovery)
  5. EQ-5 (720Hz mid hump = TS characteristic frequency)
  6. Chorus (Small Clone — essential Nirvana)
- **Bars:** Primarily 105-140 (grunge intensity sections)
- **JHS Quote:** *"Big Muff into Tube Screamer — turn the TS drive down, you don't need more distortion. Turn volume up, treble up so mids come up. Suddenly it peaks its head out, rich, thick, all the things you love about the Big Muff but stronger."*

---

## Part B Tracks (Rhythm/Countermelody)

### B1: Clean Chorus
- **JHS Source:** Chorus episode — "INXS clean DI + stereo chorus + compression"
- **Concept:** Clean DI guitar through studio compression into lush stereo BBD chorus. The 80s studio guitar sound — think "Never Tear Us Apart." Boss CE-1/CE-2 character.
- **FX Chain:**
  1. Compressor (studio compression before amp)
  2. **CLA Guitars Stereo** (Clean mode, totally pristine)
  3. Chorus+ (rich stereo chorus = CE-2 / Brigade character)
  4. EQ-5 (slight treble lift for sparkle)
  5. Compressor (final compression for evenness)
- **Bars:** Primarily 1-32, 105-120 (clean, shimmering sections)
- **JHS Quote:** *"Clean DI, stereo chorus, studio compression — that INXS sound. Shimmering, pristine, wide."*

### B2: Tremolo Reverb
- **JHS Source:** Stack episode — reverb BEFORE tremolo (breaking the rule)
- **Concept:** Convention says tremolo before reverb/delay. But in a blackface '65 Princeton, tremolo is AFTER reverb. "Take a big ambient reverb, then let tremolo pulse the decay and clean signal. Really beautiful, awesome for clean tones."
- **FX Chain:**
  1. Saturator (light breakup, never fully clean)
  2. **CLA Guitars Stereo** (Clean mode, reverb color)
  3. Reverb (big ambient wash — like Dark Star)
  4. Tremolo (pulses the reverb decay)
  5. EQ-5 (final tone shaping)
- **Bars:** Primarily 89-120 (atmospheric, pulsing sections)
- **JHS Quote:** *"Reverb before tremolo — just like a blackface Princeton. Take a big ambient reverb, let tremolo pulse the decay. Peanut butter and jelly."*

### B3: Boost Cascade
- **JHS Source:** Stack episode — "two boost pedals = DIY custom overdrive"
- **Concept:** Two clean boosts cascading into each other creates an overdrive, just like how tube amps work — gain stages saturating into each other. "Infinitely tweakable, great for people who want something outside the box of Tube Screamers."
- **FX Chain:**
  1. Tool (first boost stage — gain control)
  2. Saturator (second boost stage — adds saturation as gain hits)
  3. Filter (tone shaping between stages)
  4. **CLA Guitars Stereo** (Crunch mode, edge of breakup)
  5. EQ-5 (final shaping)
- **Bars:** Primarily 33-72, 141-160 (driving rhythm sections)
- **JHS Quote:** *"Take two boost pedals, combine them. It's a DIY overdrive. The first knob becomes a master volume, the second controls drive. Infinitely tweakable, fantastic."*

### B4: Ambient Delay Verb
- **JHS Source:** Stack episode — "quarter delay into modulated reverb"
- **Concept:** Faint-but-present quarter note delay bouncing into Boss RV-5 style modulated reverb. "One of the best sounds out there." Keep modulation and effect level low — don't wash it out. "If you do it in a faint way, it's really special."
- **FX Chain:**
  1. EQ-5 (high-frequency air for clarity)
  2. **CLA Guitars Stereo** (Clean mode, pristine)
  3. Delay-4 (quarter note delay, moderate feedback)
  4. Chorus (modulation on the delay/reverb tail)
  5. Reverb (modulated reverb wash)
  6. Micro-pitch (extra width and shimmer)
- **Bars:** Primarily 49-88, 161-184 (ambient, spacious sections)
- **JHS Quote:** *"Quarter note delay into modulated reverb — one of the best sounds out there. Keep the modulation faint. If you do it in a faint way, it's really special."*

---

## CLA Guitars Stereo Configuration Guide

Each WaveShell instance loads CLA Guitars Stereo. Configure based on track role:

| Track | Guitar Mode | Bass | Treble | Compress | Reverb | Delay | Pitch |
|-------|-------------|------|--------|----------|--------|-------|-------|
| A1 | Crunch | +3 Blue | +2 Green | +4 Green | 0 Clear | 0 Clear | 0 Clear |
| A2 | Heavy | +5 Red | +1 Blue | +6 Red | 0 Clear | 0 Clear | 0 Clear |
| A3 | Clean | 0 Clear | +4 Green | +2 Green | +2 Green | +3 Blue | +2 Green |
| A4 | Heavy | +4 Blue | +3 Red | +5 Blue | 0 Clear | 0 Clear | 0 Clear |
| B1 | Clean | +1 Green | +3 Green | +3 Green | +1 Green | 0 Clear | +2 Blue |
| B2 | Clean | +2 Blue | +1 Green | +2 Green | +5 Blue | 0 Clear | 0 Clear |
| B3 | Crunch | +3 Green | +2 Blue | +3 Blue | 0 Clear | 0 Clear | 0 Clear |
| B4 | Clean | 0 Clear | +2 Green | +1 Green | +3 Blue | +4 Blue | +3 Blue |

**Color meanings (from CLA Guitars manual):**
- Bass: Clear=bypass, Green=Sub, Blue=Lower, Red=Upper
- Treble: Clear=bypass, Green=Bite, Blue=Top, Red=Roof
- Compress: Clear=bypass, Green=Push, Blue=Spank, Red=Wall
- Reverb: Clear=Mute, Green=Club, Blue=Hall, Red=Arena
- Delay: Clear=Mute, Green=1/8th, Blue=Edge(dotted 1/8), Red=Quarter
- Pitch: Clear=Mute, Green=Stereo, Blue=Wide, Red=Spreader

---

## Track Distribution Map

How the full parts are distributed across the 4 tracks (bar ranges, with overlaps):

### Part A Distribution
```
Bar:  1----16----32----48----64----72----88----104---120---140---160---176-184
A1:   ████████████████████                              ████████████
A2:                               ████████      ████████
A3:                   ████████████        ████████
A4:                                               ██████████████
```

### Part B Distribution
```
Bar:  1----16----32----48----64----72----88----104---120---140---160---176-184
B1:   ██████████████                      ████████
B2:                               ████████████████████
B3:                   ████████████████                  ████████████
B4:                         ██████████████        ██████████████████████
```

Note: Overlaps (bars where 2+ tracks play simultaneously) create texture and blend.
Part A and Part B distributions are completely independent of each other.
