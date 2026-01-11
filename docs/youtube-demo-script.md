# Groove Link: Vibe Coding Music Production - YouTube Demo Script

> A demonstration of using Claude Code to produce music in Bitwig Studio via natural language prompts.

---

## Introduction

**[NARRATION - 30 seconds]**

What if you could describe a song and have it appear in your DAW? Not generated audio - actual tracks, actual instruments, actual signal chains. Real presets you can tweak, real MIDI you can edit, real mix buses you can adjust. This is Groove Link. It's a bridge between Claude Code and Bitwig Studio. You write prompts, I interpret them, and Bitwig builds the session. Let's make some music.

---

## Demo 1: The Simplest Possible Thing

**[PROMPT]**
```yaml
song:
  title: One Note
  tempo: 120

tracks:
  piano:
    instrument: Concert Grand
```

**[NARRATION - 20 seconds]**

That's it. One track, one instrument. No effects, no complexity. The system finds "Concert Grand" in Bitwig's preset library using fuzzy search, creates an instrument track, and loads it. You could play this right now. Most tutorials start complicated. I'm starting with the minimum viable song. One instrument. Let's add a second.

---

## Demo 2: A Simple Duet

**[PROMPT]**
```yaml
song:
  title: Two Voices
  tempo: 92
  key: D minor

tracks:
  piano:
    instrument: Felt Piano
    fx:
      - Smooth Compression

  bass:
    instrument: Upright Bass
    fx:
      - Analogue Compressor
```

**[NARRATION - 25 seconds]**

Two instruments, each with one effect. The bass gets compression because bass always gets compression. The piano gets "Smooth Compression" which is a different preset - gentler, more transparent. Notice I didn't specify whether these are Bitwig devices or presets or plugins. The resolver figures it out. It searches presets first, then base devices, then plugins. You can force it with hints, but usually you don't need to.

---

## Demo 3: Adding a Master Bus

**[PROMPT]**
```yaml
song:
  title: Proper Gain Staging
  tempo: 100

tracks:
  keys:
    instrument: Electric Piano
    fx:
      - Chorus
      - Tape-Machine

  master:
    fx:
      - EQ-5
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

The "master" track is special. It doesn't create a new track - it adds effects to the master bus. Every song should have something on the master. At minimum, a limiter so nothing clips. I'm using EQ-5 here not to shape tone but to have visual feedback while mixing. Peak Limiter catches transients. This is hygiene, not creativity. But hygiene matters. Clip your master once in a live demo and you'll never forget it.

---

## Demo 4: Your First Shared FX Bus

**[PROMPT]**
```yaml
song:
  title: Room Tone
  tempo: 85
  key: G

tracks:
  piano:
    instrument: Intimate Piano
    fx:
      - Soft Saturation

  strings:
    instrument: Chamber Strings
    fx:
      - EQ-5

  room:
    receives:
      - piano: pre
      - strings: pre
    fx:
      - Room One
      - Tape-Machine

  master:
    fx:
      - Dynamic EQ
      - Peak Limiter
```

**[NARRATION - 35 seconds]**

Here's where it gets interesting. The "room" track doesn't have an instrument. It has "receives" - it's pulling audio from piano and strings through Audio Receiver devices. "Pre" means pre-fader, so the reverb amount stays constant even if you automate volume. This is how professionals mix. They don't put reverb on every track. They send multiple tracks to a shared reverb bus. Same reverb, same room, same space. Coherent mix. Also cheaper on CPU. One reverb instance instead of five.

---

## Demo 5: Parallel Compression on Drums

**[PROMPT]**
```yaml
song:
  title: Punchy Kit
  tempo: 118

tracks:
  drums:
    instrument: Acoustic Kit
    fx:
      - Transient Shaper

  drum_crush:
    receives:
      - drums: post
    fx:
      - Hard Compression
      - Saturator

  master:
    fx:
      - EQ-5
      - Focused Mastering
```

**[NARRATION - 30 seconds]**

Parallel compression. Also called New York compression. You take your drums, send them to a bus, and destroy them with compression. Then blend the destroyed signal with the clean signal. You get punch AND dynamics. The "post" setting means if you turn down the drum fader, the crush bus follows. This technique came from engineers in the 80s who were trying to make drums cut through dense mixes. It worked then. It works now. It'll work forever.

---

## Demo 6: Industrial Starter Kit

**[PROMPT]**
```yaml
song:
  title: Rust and Static
  tempo: 130

tracks:
  lead:
    instrument: FM Aggression
    fx:
      - Distortion
      - Flanger

  bass:
    instrument: Mono Growl
    fx:
      - Amp
      - Cabinet

  drums:
    instrument: 808 Kit
    fx:
      - Bit-8
      - Transient Shaper

  noise:
    instrument: Noise Generator
    fx:
      - Gate
      - Delay+

  master:
    fx:
      - Dynamic EQ
      - Hard Clipper
```

**[NARRATION - 35 seconds]**

We're leaving pretty behind. Industrial music is about textures that hurt. The noise generator is literally just noise, gated rhythmically. The drums go through Bit-8 for that crunchy, reduced bit depth sound. The bass goes through amp and cabinet simulation like a guitar - because in industrial, bass IS a guitar, conceptually. And on the master? Hard clipper. Not a limiter. A clipper. We want flat tops on those transients. Ministry, Nine Inch Nails, KMFDM - this is the toolkit.

---

## Demo 7: 90s Jungle Influenced D&B

**[PROMPT]**
```yaml
song:
  title: Amen Parliament
  tempo: 172

tracks:
  breaks:
    instrument: Jungle Breaks
    fx:
      - Transient Shaper
      - Distortion

  bass:
    instrument: Reese Bass
    fx:
      - Chorus
      - Saturator
      - EQ-5

  pad:
    instrument: Atmospheric Pad
    fx:
      - Phaser
      - Delay+

  stab:
    instrument: Hoover
    fx:
      - Reverb

  master:
    fx:
      - EQ-5
      - Compressor
      - Peak Limiter
```

**[NARRATION - 40 seconds]**

172 BPM. That's jungle tempo. The Amen break, the Reese bass, the hoover stab - these are the holy trinity. The Reese bass is named after Kevin Saunderson's track "Just Want Another Chance" - a detuned saw wave that phases against itself. The hoover is that vacuum cleaner sound from Belgian techno that somehow ended up defining an entire genre. Jungle took these elements, chopped them up, and ran them at speeds that made house DJs nervous. This isn't a genre that aged. It's a genre that keeps coming back because 172 BPM with chopped breaks just hits different.

---

## Demo 8: Minimal Techno

**[PROMPT]**
```yaml
song:
  title: Funktional
  tempo: 128

tracks:
  kick:
    instrument: Techno Kick
    fx:
      - EQ-5

  hats:
    instrument: Minimal Hats
    fx:
      - Transient Shaper

  perc:
    instrument: Percussion
    fx:
      - Delay+
      - Filter

  bass:
    instrument: Sine Bass
    fx:
      - Saturator

  master:
    fx:
      - Compressor
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

Minimal techno is the opposite of industrial. It's not about how much you can add. It's about how much you can remove while still having a track. Robert Hood, Richie Hawtin, Ricardo Villalobos - these producers built careers on restraint. A kick, some hats, a sine bass, maybe one percussion element with delay. That's it. The groove comes from the space between the notes. If you can't make four elements interesting, adding more won't help.

---

## Demo 9: Shoegaze Wall

**[PROMPT]**
```yaml
song:
  title: Everything Blurs
  tempo: 76
  key: E

tracks:
  guitar_1:
    instrument: Clean Electric
    fx:
      - Chorus
      - Reverb
      - Delay+
      - Reverb

  guitar_2:
    instrument: Clean Electric
    fx:
      - Flanger
      - Reverb
      - Distortion
      - Reverb

  bass:
    instrument: Bass Guitar
    fx:
      - Chorus
      - Amp

  drums:
    instrument: Lo-Fi Kit
    fx:
      - Reverb
      - Compressor

  wash:
    receives:
      - guitar_1: pre
      - guitar_2: pre
    fx:
      - Shimmer Reverb
      - Delay+

  master:
    fx:
      - EQ-5
      - Soft Compression
```

**[NARRATION - 35 seconds]**

My Bloody Valentine invented a sound where guitars stop being guitars and become weather. Two reverbs per guitar isn't a mistake - it's the point. The wash bus takes both guitars and drowns them in more reverb. Shoegaze is the only genre where "too much reverb" is structurally impossible. Kevin Shields spent two years making Loveless. He bankrupted Creation Records. He also made one of the most influential albums ever. This template won't get you there, but it'll get you the palette.

---

## Demo 10: Chicago House

**[PROMPT]**
```yaml
song:
  title: Warehouse Foundation
  tempo: 122

tracks:
  kick:
    instrument: House Kick
    fx:
      - EQ-5

  bass:
    instrument: 303 Bass
    fx:
      - Filter
      - Distortion

  chords:
    instrument: Classic Keys
    fx:
      - Chorus
      - Phaser

  clap:
    instrument: Clap
    fx:
      - Reverb

  hats:
    instrument: Open Hats

  master:
    fx:
      - EQ-5
      - Compressor
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

Chicago house. Frankie Knuckles, Ron Hardy, the Warehouse. 122 BPM is the tempo where heads nod involuntarily. The 303 bass - originally a failed bass guitar replacement - became the voice of acid house when someone turned the resonance up and the filter started screaming. Classic keys, probably a Rhodes or Wurlitzer sound. A clap with reverb. Open hats. This is the template that launched a thousand subgenres. Every house track since 1985 is a variation on this.

---

## Demo 11: West Coast G-Funk

**[PROMPT]**
```yaml
song:
  title: Six Four
  tempo: 92

tracks:
  keys:
    instrument: Moog Bass
    fx:
      - Chorus
      - Phaser

  synth:
    instrument: High Synth Lead
    fx:
      - Portamento
      - Chorus

  drums:
    instrument: Hip Hop Kit
    fx:
      - Compressor

  talk_box:
    instrument: Talk Box
    fx:
      - EQ-5

  master:
    fx:
      - EQ-5
      - Soft Compression
      - Peak Limiter
```

**[NARRATION - 35 seconds]**

Dr. Dre took Parliament samples and slowed them down. The Chronic changed everything. G-Funk is about that lazy, sun-drenched, lowrider bounce. 92 BPM - slow enough to be smooth but fast enough to have swagger. The Moog bass is doing Bootsy Collins impressions. The high synth lead with portamento - that's the sound that makes you think of palm trees and hydraulics. The talk box because someone's gotta do the robot voice. Warren G, Snoop, Nate Dogg - this sound defined an era.

---

## Demo 12: UK Garage

**[PROMPT]**
```yaml
song:
  title: Two Step Swing
  tempo: 130

tracks:
  drums:
    instrument: Garage Kit
    fx:
      - Transient Shaper
      - Compressor

  bass:
    instrument: Sub Bass
    fx:
      - EQ-5

  organ:
    instrument: Organ Stab
    fx:
      - Reverb

  vocal_chop:
    instrument: Vocal Chops
    fx:
      - Delay+
      - Filter

  master:
    fx:
      - Dynamic EQ
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

UK Garage is house music's hyperactive cousin. The two-step rhythm shuffles where house plods. MJ Cole, Todd Edwards, Artful Dodger - they took American garage, sped it up, added skippy drums, and created something London couldn't stop dancing to. The bass is sub, meaning you feel it more than hear it. Vocal chops because garage loves manipulating voices into percussive elements. This sound eventually mutated into dubstep, but that's a different prompt.

---

## Demo 13: Bristol Trip-Hop

**[PROMPT]**
```yaml
song:
  title: Cigarette Smoke and Vinyl
  tempo: 84
  key: D minor

tracks:
  drums:
    instrument: Dusty Breaks
    fx:
      - Lo-Fi
      - Compressor

  bass:
    instrument: Upright Bass
    fx:
      - Saturator
      - EQ-5

  rhodes:
    instrument: Vintage Rhodes
    fx:
      - Tremolo
      - Tape-Machine

  strings:
    instrument: String Section
    fx:
      - Reverb
      - Filter

  scratch:
    instrument: Turntable FX
    fx:
      - EQ-5

  master:
    fx:
      - Tape-Machine
      - EQ-5
      - Soft Compression
```

**[NARRATION - 35 seconds]**

Massive Attack, Portishead, Tricky. Bristol in the 90s was making music that sounded like film noir felt. Dusty breaks run through lo-fi processing to simulate old records. Upright bass because trip-hop loves jazz instrumentation. The Rhodes with tremolo and tape saturation - that's the sound of 3 AM in a city that never quite wakes up. Tape-Machine on the master because this entire genre is about sounding like a lost recording from 1972.

---

## Demo 14: Detroit Techno

**[PROMPT]**
```yaml
song:
  title: Model 500
  tempo: 130

tracks:
  kick:
    instrument: TR-909 Kick
    fx:
      - EQ-5

  snare:
    instrument: TR-909 Snare
    fx:
      - Reverb

  hats:
    instrument: TR-909 Hats

  bass:
    instrument: TB-303
    fx:
      - Filter
      - Distortion

  strings:
    instrument: String Machine
    fx:
      - Chorus
      - Reverb

  master:
    fx:
      - EQ-5
      - Compressor
      - Peak Limiter
```

**[NARRATION - 35 seconds]**

Juan Atkins, Derrick May, Kevin Saunderson. The Belleville Three. They heard Kraftwerk and said "what if this was funky?" Detroit techno is machine music with soul. The 909 is the heartbeat - that kick, that snare, those hi-hats. The 303 is the voice. But the secret ingredient is the string machine. Strings from a Juno or a Solina, washed in chorus and reverb. That's what makes Detroit techno emotional when it could just be mechanical. It's the difference between robots working and robots dreaming.

---

## Demo 15: 2000s Blog House

**[PROMPT]**
```yaml
song:
  title: MySpace Banger
  tempo: 128

tracks:
  bass:
    instrument: Distorted Bass
    fx:
      - Amp
      - Filter
      - Compressor

  drums:
    instrument: 909 Kit
    fx:
      - Transient Shaper
      - Saturator

  lead:
    instrument: Saw Lead
    fx:
      - Filter
      - Distortion
      - Delay+

  vocals:
    instrument: Vocal Sample
    fx:
      - Filter
      - Sidechain Compressor

  master:
    fx:
      - EQ-5
      - Hard Clipper
```

**[NARRATION - 30 seconds]**

Justice, MSTRKRFT, Boys Noize. Blog house was the sound of the late 2000s internet - loud, distorted, and uncompromising. Everything goes through distortion. The bass clips. The drums clip. The lead clips. The master clipper makes sure it all clips together. This was music for blogs before streaming existed. If your track didn't sound crushed, you weren't trying. Ed Banger Records built an empire on this aesthetic.

---

## Demo 16: Doom Metal

**[PROMPT]**
```yaml
song:
  title: Funeral Pace
  tempo: 55
  key: B minor

tracks:
  guitar_left:
    instrument: High Gain Guitar
    fx:
      - Amp
      - Cabinet
      - EQ-5

  guitar_right:
    instrument: High Gain Guitar
    fx:
      - Amp
      - Cabinet
      - EQ-5

  bass:
    instrument: Bass Guitar
    fx:
      - Amp
      - Cabinet
      - Distortion

  drums:
    instrument: Heavy Kit
    fx:
      - Compressor
      - Reverb

  drone:
    instrument: Drone Synth
    fx:
      - Reverb

  master:
    fx:
      - EQ-5
      - Compressor
```

**[NARRATION - 35 seconds]**

55 BPM. That's funeral pace. Electric Wizard, Sleep, Sunn O))) - doom metal is heavy music that forgot to move. Two guitars panned left and right, both crushing. Bass through distortion because in doom, the bass doesn't support, it attacks. The drone synth fills the frequencies your ears don't consciously hear but your chest feels. Doom isn't a tempo. It's a philosophy. Everything slow. Everything loud. Everything crushing.

---

## Demo 17: 808s and Heartbreak Era

**[PROMPT]**
```yaml
song:
  title: Vocoded Sadness
  tempo: 80

tracks:
  drums:
    instrument: 808 Kit
    fx:
      - EQ-5

  bass:
    instrument: 808 Sub
    fx:
      - Saturator

  synth:
    instrument: Soft Pad
    fx:
      - Reverb
      - Delay+

  voice:
    instrument: Vocoder
    fx:
      - Reverb
      - Delay+

  master:
    fx:
      - EQ-5
      - Soft Compression
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

Kanye made sadness sound expensive. The 808 isn't a drum machine here - it's an emotional palette. Long 808 kicks that sustain like sighs. The vocoder makes the voice less human, which somehow makes it more emotional. Pads with reverb and delay because loneliness needs space to echo. This album changed hip hop. Before 808s and Heartbreak, rappers couldn't be vulnerable. After it, Drake existed.

---

## Demo 18: Punk Rock Three Piece

**[PROMPT]**
```yaml
song:
  title: Two Minutes of Fury
  tempo: 180

tracks:
  guitar:
    instrument: Punk Guitar
    fx:
      - Amp
      - Cabinet

  bass:
    instrument: Punk Bass
    fx:
      - Amp
      - Distortion

  drums:
    instrument: Punk Kit
    fx:
      - Compressor
      - Transient Shaper

  master:
    fx:
      - EQ-5
      - Hard Clipper
```

**[NARRATION - 25 seconds]**

Three instruments. 180 BPM. Two minutes or less. The Ramones didn't invent punk but they perfected the template. One guitar sound - amp and cabinet, nothing else. Bass through distortion because punk bass is just another guitar. Drums compressed into a wall. Hard clipper on the master because punk isn't supposed to sound good. It's supposed to sound urgent.

---

## Demo 19: Ambient Drone

**[PROMPT]**
```yaml
song:
  title: Cathedral
  tempo: 60
  key: E

tracks:
  drone_1:
    instrument: Drone Pad
    fx:
      - Reverb
      - Delay+
      - Reverb

  drone_2:
    instrument: Evolving Texture
    fx:
      - Chorus
      - Reverb

  harmonic:
    instrument: Glass Harmonics
    fx:
      - Reverb
      - Filter

  space:
    receives:
      - drone_1: pre
      - drone_2: pre
      - harmonic: pre
    fx:
      - Shimmer Reverb
      - Delay+

  master:
    fx:
      - EQ-5
      - Soft Compression
```

**[NARRATION - 30 seconds]**

Brian Eno asked what music would sound like if it wasn't going anywhere. Ambient drone is the answer. Multiple reverbs in series because the sound should never stop reflecting. The space bus takes everything and adds more reverb on top. This is music for airports, for cathedrals, for staring at the ceiling at 4 AM. Stars of the Lid, Eluvium, Tim Hecker - they proved that texture without rhythm is still music.

---

## Demo 20: Trap Production

**[PROMPT]**
```yaml
song:
  title: Atlanta Pressure
  tempo: 140

tracks:
  kick:
    instrument: Trap Kick
    fx:
      - EQ-5

  hats:
    instrument: Trap Hats
    fx:
      - Transient Shaper

  snare:
    instrument: Trap Snare
    fx:
      - Reverb

  bass:
    instrument: 808 Sub
    fx:
      - Distortion
      - EQ-5

  keys:
    instrument: Dark Piano
    fx:
      - Reverb

  master:
    fx:
      - Dynamic EQ
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

Trap is the sound of Atlanta conquering global pop. The hi-hats do triplet rolls that human hands can't play. The 808 sub extends below the frequency response of most speakers - you need a subwoofer or you're missing the point. The snare has reverb because trap snares should echo. Lex Luger, Metro Boomin, Zaytoven - they built a template that every producer on earth has copied.

---

## Demo 21: Post-Punk Angular

**[PROMPT]**
```yaml
song:
  title: Wire Tension
  tempo: 140

tracks:
  guitar:
    instrument: Clean Electric
    fx:
      - Chorus
      - Delay+
      - Flanger

  bass:
    instrument: Bass Guitar
    fx:
      - Distortion
      - Chorus

  drums:
    instrument: Tight Kit
    fx:
      - Gate
      - Compressor

  synth:
    instrument: Cold Synth
    fx:
      - Filter
      - Delay+

  master:
    fx:
      - EQ-5
      - Compressor
```

**[NARRATION - 30 seconds]**

Wire, Gang of Four, Joy Division. Post-punk took punk's energy and added angularity. The guitar is clean but processed - chorus and flanger because post-punk guitars should shimmer and phase. The bass is driving the song more than the guitar. Drums are tight and gated, almost mechanical. The synth is cold because post-punk synths are always cold. This is punk that read too many books.

---

## Demo 22: Dubstep (Pre-Brostep)

**[PROMPT]**
```yaml
song:
  title: South London Weight
  tempo: 140

tracks:
  drums:
    instrument: Dubstep Kit
    fx:
      - Compressor
      - EQ-5

  sub:
    instrument: Sub Bass
    fx:
      - Filter
      - Saturator

  wobble:
    instrument: Wobble Bass
    fx:
      - Filter
      - Distortion

  atmosphere:
    instrument: Dark Pad
    fx:
      - Reverb
      - Delay+

  master:
    fx:
      - Dynamic EQ
      - Peak Limiter
```

**[NARRATION - 35 seconds]**

Before Skrillex, dubstep was dark, spacious, and heavy in a different way. Burial, Skream, Benga - they made music for 3 AM in South London. The sub bass is separate from the wobble bass because they do different jobs. Sub provides weight you feel in your chest. The wobble provides movement. Atmosphere is crucial - those reverbed pads that make the space feel like a warehouse at night. This is dubstep before America got hold of it.

---

## Demo 23: Synthwave

**[PROMPT]**
```yaml
song:
  title: Neon Highway
  tempo: 118

tracks:
  bass:
    instrument: Analog Bass
    fx:
      - Chorus
      - Compressor

  drums:
    instrument: Linn Drum Kit
    fx:
      - Reverb
      - Gate

  lead:
    instrument: Saw Lead
    fx:
      - Chorus
      - Delay+

  pad:
    instrument: Warm Pad
    fx:
      - Chorus
      - Reverb

  arp:
    instrument: Arpeggio Synth
    fx:
      - Delay+
      - Filter

  master:
    fx:
      - EQ-5
      - Tape-Machine
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

Synthwave is nostalgia for a past that never existed. The LinnDrum because that's what every 80s hit used. Chorus on everything because the 80s were drenched in chorus. The arp running through delay because arpeggios should echo forever. Tape-Machine on the master because this should sound like a VHS tape. Kavinsky, Perturbator, Carpenter Brut - they made a career out of remembering things that didn't happen.

---

## Demo 24: Noise Rock

**[PROMPT]**
```yaml
song:
  title: Ear Bleeding Optimism
  tempo: 160

tracks:
  guitar_1:
    instrument: Heavily Distorted
    fx:
      - Amp
      - Distortion
      - Distortion

  guitar_2:
    instrument: Feedback Machine
    fx:
      - Amp
      - Fuzz

  bass:
    instrument: Bass Guitar
    fx:
      - Distortion
      - Amp

  drums:
    instrument: Loud Kit
    fx:
      - Compressor
      - Saturator

  master:
    fx:
      - Hard Clipper
```

**[NARRATION - 25 seconds]**

Lightning Bolt, Melt-Banana, Big Black. Noise rock is what happens when volume becomes composition. Two distortions in series on the guitar because one isn't enough. Fuzz on the second guitar because fuzz is different than distortion - it's more broken, more wrong. Hard clipper on the master with nothing else. No EQ, no subtle compression. This genre doesn't want to sound good. It wants to sound like damage.

---

## Demo 25: Bossa Nova

**[PROMPT]**
```yaml
song:
  title: Ipanema Adjacent
  tempo: 140
  key: F

tracks:
  guitar:
    instrument: Nylon Guitar
    fx:
      - EQ-5
      - Reverb

  bass:
    instrument: Upright Bass
    fx:
      - Compressor

  piano:
    instrument: Jazz Piano
    fx:
      - Tape-Machine

  drums:
    instrument: Brush Kit
    fx:
      - Reverb

  master:
    fx:
      - EQ-5
      - Soft Compression
```

**[NARRATION - 25 seconds]**

Antonio Carlos Jobim made sadness sound like sunshine. Bossa nova is samba slowed down and made intimate. Nylon guitar because steel strings are too aggressive. Upright bass with gentle compression. Brush kit because bossa drums should whisper. The tempo says 140 but it feels slower because the groove is laid back. This is Sunday morning music for people who have their life together.

---

## Demo 26: Breakcore Chaos

**[PROMPT]**
```yaml
song:
  title: Chopped and Destroyed
  tempo: 200

tracks:
  breaks:
    instrument: Amen Break
    fx:
      - Bit-8
      - Distortion
      - Filter

  bass:
    instrument: Distorted Bass
    fx:
      - Amp
      - Filter

  lead:
    instrument: Harsh Lead
    fx:
      - Distortion
      - Delay+

  noise:
    instrument: Noise Generator
    fx:
      - Gate
      - Filter

  glitch:
    instrument: Glitch Textures
    fx:
      - Delay+
      - Bit-8

  master:
    fx:
      - Hard Clipper
```

**[NARRATION - 30 seconds]**

Venetian Snares, Igorrr, Ruby My Dear. Breakcore takes jungle and feeds it through a wood chipper. 200 BPM because slower would be too easy to follow. The Amen break chopped into fragments smaller than recognition. Bit-8 for extra crunch. A noise track because breakcore needs texture that sounds like machines dying. No EQ on the master. Just a clipper. This is music that hates your ears but you can't stop listening.

---

## Demo 27: 70s Prog Rock

**[PROMPT]**
```yaml
song:
  title: Side Two of the Concept Album
  tempo: 84
  key: C# minor

tracks:
  mellotron:
    instrument: Mellotron Strings
    fx:
      - Chorus
      - Tape-Machine

  organ:
    instrument: Hammond Organ
    fx:
      - Rotary Speaker
      - Amp

  synth:
    instrument: Moog Lead
    fx:
      - Portamento
      - Delay+

  bass:
    instrument: Bass Guitar
    fx:
      - Chorus
      - Amp

  drums:
    instrument: Acoustic Kit
    fx:
      - Reverb
      - Compressor

  master:
    fx:
      - Tape-Machine
      - EQ-5
      - Soft Compression
```

**[NARRATION - 35 seconds]**

Yes, Genesis, King Crimson. Progressive rock was what happened when rock musicians decided they were classical composers. The Mellotron - that creepy string sound that defined a decade. Hammond organ through a Leslie rotary speaker because the doppler effect is prog rock's secret weapon. Moog with portamento for leads that slide between notes. Tape-Machine on master because prog rock should sound like it was recorded in 1973 even when it wasn't.

---

## Demo 28: Lo-Fi Hip Hop

**[PROMPT]**
```yaml
song:
  title: Beats to Study To
  tempo: 85

tracks:
  drums:
    instrument: Lo-Fi Kit
    fx:
      - Lo-Fi
      - Compressor

  bass:
    instrument: Electric Bass
    fx:
      - EQ-5

  piano:
    instrument: Dusty Piano
    fx:
      - Vinyl Noise
      - Filter
      - Tape-Machine

  vinyl:
    instrument: Vinyl Crackle
    fx:
      - Filter

  master:
    fx:
      - Tape-Machine
      - EQ-5
      - Soft Compression
```

**[NARRATION - 25 seconds]**

Nujabes made homework tolerable. Lo-fi hip hop is jazz samples run through filters until they sound like memories. The vinyl crackle is a separate track because nostalgia needs to be mixed properly. Lo-fi on the drums. Tape-Machine on the piano. Tape-Machine on the master. This is music that's trying to sound worse on purpose and somehow that makes it better.

---

## Demo 29: Gabber

**[PROMPT]**
```yaml
song:
  title: Rotterdam Aggression
  tempo: 180

tracks:
  kick:
    instrument: Gabber Kick
    fx:
      - Distortion
      - EQ-5

  snare:
    instrument: Industrial Snare
    fx:
      - Distortion

  hats:
    instrument: Harsh Hats
    fx:
      - Transient Shaper

  bass:
    instrument: Distorted Bass
    fx:
      - Amp
      - Filter

  lead:
    instrument: Hoover
    fx:
      - Distortion

  master:
    fx:
      - Hard Clipper
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

Rotterdam in the early 90s decided techno wasn't hard enough. Gabber is 180 BPM or faster, with a kick drum that sounds like a punch to the chest. Everything distorted. The hoover lead because gabber loves that sound. Hard clipper into peak limiter on the master because gabber should hurt. This is music for people who think industrial is too gentle. Rotterdam Terror Corps, Neophyte, Angerfist - this is the sound of a city choosing violence.

---

## Demo 30: Intentionally Bad - Bedroom Producer Mistakes

**[PROMPT]**
```yaml
song:
  title: My First Beat
  tempo: 128

tracks:
  drums:
    instrument: Stock Kit
    fx:
      - Reverb
      - Reverb
      - Reverb

  bass:
    instrument: Default Bass
    fx:
      - Reverb

  lead:
    instrument: Preset Lead
    fx:
      - Reverb

  pad:
    instrument: Generic Pad
    fx:
      - Reverb

  master:
    fx:
      - Reverb
```

**[NARRATION - 30 seconds]**

This is what NOT to do. Reverb on everything including the master. The low end will be mud. The transients will be gone. The mix will be a washy mess with no definition. I see this mistake constantly from new producers. Reverb feels like magic when you first discover it. Everything sounds bigger, more professional. Until you put it on everything and wonder why your mix sounds like it's underwater. Reverb is not a volume knob.

---

## Demo 31: Krautrock Motorik

**[PROMPT]**
```yaml
song:
  title: Autobahn Adjacent
  tempo: 110

tracks:
  drums:
    instrument: Motorik Kit
    fx:
      - Gate
      - Compressor

  bass:
    instrument: Electric Bass
    fx:
      - Chorus

  synth_1:
    instrument: Sequencer Synth
    fx:
      - Filter
      - Delay+

  synth_2:
    instrument: Evolving Pad
    fx:
      - Phaser
      - Reverb

  flute:
    instrument: Electronic Flute
    fx:
      - Delay+

  master:
    fx:
      - Tape-Machine
      - EQ-5
      - Compressor
```

**[NARRATION - 30 seconds]**

Kraftwerk, Neu!, Can. Motorik is the driving rhythm that defines krautrock - that hypnotic, unchanging beat that sounds like driving on an infinite highway. The drums are gated tight. The bass provides the pulse. Synths sequencing against each other creating polyrhythms through repetition. Flute because krautrock always has unexpected acoustic elements. This is German efficiency applied to psychedelia.

---

## Demo 32: Riddim Dubstep

**[PROMPT]**
```yaml
song:
  title: Minimal Aggression
  tempo: 150

tracks:
  drums:
    instrument: Riddim Kit
    fx:
      - Transient Shaper
      - Compressor

  sub:
    instrument: Sub Bass
    fx:
      - EQ-5

  mid_bass:
    instrument: Growl Bass
    fx:
      - Distortion
      - Filter
      - Saturator

  master:
    fx:
      - Dynamic EQ
      - Hard Clipper
      - Peak Limiter
```

**[NARRATION - 25 seconds]**

Riddim took dubstep and removed everything except the bass. Minimal drums. Almost no melodic content. Just that mid-bass growl doing rhythmic patterns. The sub and mid-bass are separate because they need different processing. The mid-bass gets distorted and filtered while the sub stays clean. This is music for crowds who want to headbang, not think.

---

## Demo 33: Jazz Fusion

**[PROMPT]**
```yaml
song:
  title: Return to Weather
  tempo: 108
  key: Bb

tracks:
  rhodes:
    instrument: Vintage Rhodes
    fx:
      - Phaser
      - Chorus
      - Amp

  bass:
    instrument: Fretless Bass
    fx:
      - Chorus
      - Compressor

  drums:
    instrument: Fusion Kit
    fx:
      - Reverb
      - Compressor

  synth:
    instrument: Oberheim Pad
    fx:
      - Phaser
      - Delay+

  guitar:
    instrument: Clean Jazz Guitar
    fx:
      - Chorus
      - Delay+

  master:
    fx:
      - EQ-5
      - Soft Compression
```

**[NARRATION - 30 seconds]**

Weather Report, Herbie Hancock, Return to Forever. Fusion was jazz musicians deciding they wanted to get weird with synthesizers. Rhodes through phaser because that's the Herbie Hancock sound. Fretless bass with chorus for that Jaco Pastorius tone. The Oberheim pad for that creamy analog warmth. Fusion is jazz that went to music school and then forgot everything on purpose.

---

## Demo 34: Grime

**[PROMPT]**
```yaml
song:
  title: East London Pressure
  tempo: 140

tracks:
  drums:
    instrument: Grime Kit
    fx:
      - Transient Shaper
      - EQ-5

  bass:
    instrument: Square Bass
    fx:
      - Filter
      - Distortion

  lead:
    instrument: Grime Lead
    fx:
      - Filter
      - Delay+

  strings:
    instrument: Dark Strings
    fx:
      - Filter

  master:
    fx:
      - EQ-5
      - Compressor
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

Wiley, Dizzee Rascal, Skepta. Grime is UK garage's angry younger sibling. 140 BPM because that's the tempo where MCs can still flow but everything feels urgent. Square bass because grime bass is digital and aggressive. That lead synth - often called a "riff" - is the melodic hook. Dark strings because grime loves minor keys and tension. This is the sound of East London tower blocks.

---

## Demo 35: Psychedelic Rock

**[PROMPT]**
```yaml
song:
  title: Expanding Mind
  tempo: 100
  key: E

tracks:
  guitar:
    instrument: Clean Electric
    fx:
      - Fuzz
      - Phaser
      - Reverb
      - Delay+

  bass:
    instrument: Bass Guitar
    fx:
      - Fuzz
      - Chorus

  organ:
    instrument: Farfisa Organ
    fx:
      - Tremolo
      - Reverb

  drums:
    instrument: Acoustic Kit
    fx:
      - Reverb
      - Compressor

  sitar:
    instrument: Sitar
    fx:
      - Reverb
      - Filter

  master:
    fx:
      - Tape-Machine
      - EQ-5
      - Compressor
```

**[NARRATION - 30 seconds]**

The Beatles, Pink Floyd, The Doors. Psychedelic rock was the sound of the 60s trying to expand consciousness through sound. Fuzz pedals because distortion wasn't intense enough. Phaser on guitars because the swirling effect mimics certain experiences. Farfisa organ with tremolo - that queasy, wobbling sound. And of course a sitar because everything needed Indian influence in 1967. Tape saturation on master because analog warmth is mandatory.

---

## Demo 36: Vaporwave

**[PROMPT]**
```yaml
song:
  title: Plaza Forever
  tempo: 80

tracks:
  sample:
    instrument: 80s Sample
    fx:
      - Lo-Fi
      - Pitch Shifter
      - Reverb

  drums:
    instrument: TR-707 Kit
    fx:
      - Lo-Fi
      - Reverb

  bass:
    instrument: Slap Bass Sample
    fx:
      - Filter
      - Lo-Fi

  sax:
    instrument: Smooth Sax
    fx:
      - Reverb
      - Chorus

  master:
    fx:
      - Lo-Fi
      - Tape-Machine
      - EQ-5
```

**[NARRATION - 30 seconds]**

Vaporwave is dead shopping malls and late capitalism set to music. Take 80s muzak, slow it down, drench it in reverb and lo-fi processing. The TR-707 because that's the drum machine from actual 80s pop. Slap bass because that's the most 80s sound possible. Smooth sax because vaporwave loves the ghosts of yacht rock. Everything degraded, everything slowed, everything nostalgic for a future that never arrived.

---

## Demo 37: Harsh Noise Wall

**[PROMPT]**
```yaml
song:
  title: Static Monolith
  tempo: 60

tracks:
  noise_1:
    instrument: White Noise
    fx:
      - Distortion
      - Distortion
      - Filter

  noise_2:
    instrument: Feedback Generator
    fx:
      - Distortion
      - Amp

  noise_3:
    instrument: Static Texture
    fx:
      - Bit-8
      - Filter
      - Distortion

  master:
    fx:
      - Hard Clipper
```

**[NARRATION - 25 seconds]**

This barely qualifies as music and that's the point. Harsh noise wall is a genre that rejects everything - melody, rhythm, dynamics. Just a wall of static. Merzbow, Vomir, The Rita. Multiple noise sources, all distorted, all mixed into impenetrability. Is it music? Is it sound art? Is it a dare? Yes. The answer is yes.

---

## Demo 38: Neo-Soul

**[PROMPT]**
```yaml
song:
  title: Electric Lady Adjacent
  tempo: 94
  key: Ab

tracks:
  rhodes:
    instrument: Warm Rhodes
    fx:
      - Chorus
      - Phaser
      - Tape-Machine

  bass:
    instrument: Electric Bass
    fx:
      - Compressor
      - Saturator

  drums:
    instrument: Neo-Soul Kit
    fx:
      - Compressor
      - Tape-Machine

  synth:
    instrument: Vintage Synth
    fx:
      - Filter
      - Chorus

  guitar:
    instrument: Clean Electric
    fx:
      - Tremolo
      - Reverb

  master:
    fx:
      - Tape-Machine
      - EQ-5
      - Soft Compression
```

**[NARRATION - 30 seconds]**

D'Angelo, Erykah Badu, The Roots. Neo-soul took 70s funk and soul, ran it through the J Dilla production aesthetic, and made something new. The Rhodes is essential - warm, chorused, phased. Drums with tape saturation for that vintage feel. The whole mix should feel like warm vinyl. This is hip hop that studied Motown, jazz that remembers funk, soul music for people who know their samples.

---

## Demo 39: Hardstyle

**[PROMPT]**
```yaml
song:
  title: Amsterdam Euphoria
  tempo: 150

tracks:
  kick:
    instrument: Hardstyle Kick
    fx:
      - EQ-5
      - Distortion

  bass:
    instrument: Distorted Bass
    fx:
      - Filter
      - Saturator

  lead:
    instrument: Euphoric Lead
    fx:
      - Reverb
      - Delay+

  strings:
    instrument: Epic Strings
    fx:
      - Reverb

  sweep:
    instrument: Sweep FX
    fx:
      - Filter

  master:
    fx:
      - EQ-5
      - Hard Clipper
      - Peak Limiter
```

**[NARRATION - 30 seconds]**

Hardstyle is gabber that went to the gym and found euphoria. The kick has that characteristic hardstyle punch - distorted but tight. The lead is big and melodic because hardstyle wants you to feel feelings while your chest gets pounded. Euphoric strings because hardstyle loves the contrast between aggression and beauty. This is the sound of Dutch festivals, arms in the air, thousands of people moving as one.

---

## Demo 40: Experimental Disaster - Everything At Once

**[PROMPT]**
```yaml
song:
  title: Too Many Ideas
  tempo: 175

tracks:
  drums_1:
    instrument: TR-808
    fx:
      - Reverb
      - Distortion

  drums_2:
    instrument: Acoustic Kit
    fx:
      - Lo-Fi

  bass_1:
    instrument: Sub Bass
    fx:
      - Chorus

  bass_2:
    instrument: Distorted Bass
    fx:
      - Filter

  lead_1:
    instrument: Saw Lead
    fx:
      - Delay+

  lead_2:
    instrument: Square Lead
    fx:
      - Reverb

  pad_1:
    instrument: Warm Pad
    fx:
      - Chorus

  pad_2:
    instrument: Cold Pad
    fx:
      - Flanger

  piano:
    instrument: Grand Piano
    fx:
      - Reverb

  guitar:
    instrument: Clean Electric
    fx:
      - Distortion

  noise:
    instrument: Noise Generator
    fx:
      - Gate

  master:
    fx:
      - EQ-5
      - Compressor
```

**[NARRATION - 35 seconds]**

This is what happens when you can't commit. Two drum kits. Two basses. Two leads. Two pads. Piano. Guitar. Noise. Nothing matches. The tempo is wrong for most of these elements. The frequencies will clash constantly. This is a masterclass in how NOT to produce. Every new producer goes through this phase - throwing everything at the wall because you haven't learned that subtraction is more important than addition. Kill your darlings. Less is more. Delete most of these tracks.

---

## Extended Deep Dive: Production Philosophy and Practical Wisdom

**[LONG NARRATION - Approximately 60 minutes of spoken content]**

Let's talk about what we're actually doing here and why it matters.

### Part 1: What is Vibe Coding for Music Production?

The term "vibe coding" came from Andrej Karpathy's description of programming by vibes rather than by understanding every line. You write what you want, the AI figures out how to make it work, and you iterate based on what you see. It's controversial in software engineering because code that you don't understand will eventually break in ways you can't fix. But music production is different.

Music production has always been vibes. When a producer says "make it more punchy" or "give it some air" or "it needs to breathe," those aren't technical specifications. Those are vibes. The technical skills - knowing that "punchy" often means transient emphasis and compression, that "air" is high frequency EQ boost around 10-12kHz, that "breathing" usually means dynamic range and sidechain - those translate vibes into settings. But the vibes come first.

What we've built here is a translation layer. You describe what you want. The system translates that into Bitwig tracks with devices loaded and signal chains configured. You get a starting point that matches your vibe, and then you do what producers have always done: tweak, adjust, automate, and make it yours.

This is not a replacement for learning production. It's an accelerator. If you don't know what parallel compression is, you won't know to ask for it. If you don't understand why shoegaze uses multiple reverbs in series, you won't think to specify that. The prompts encode production knowledge. Better producers write better prompts.

### Part 2: Why Bitwig?

I could have built this for Ableton, Logic, Pro Tools, or any other DAW. Bitwig has specific advantages that made it the right choice.

First, Bitwig has a controller API that allows extensions to create tracks, load devices, set parameters, and interact with the browser programmatically. Not every DAW exposes this functionality. Some DAWs are essentially closed boxes that only accept MIDI input.

Second, Bitwig's modular architecture means that the signal chain concept maps cleanly to how you actually build sounds. Instrument, note effects, audio effects, sends - these are discrete concepts in Bitwig's model, not hacks layered on top of a mixer.

Third, Bitwig's preset ecosystem is surprisingly consistent. A preset named "Smooth Compression" actually does smooth compression. "Tape-Machine" sounds like tape. The naming conventions are clear enough that fuzzy search can find what you mean even when you don't remember the exact name.

The limitation is that Bitwig is the only target. If you use Ableton, this doesn't help you directly. But the concepts transfer. The prompt patterns work for any DAW if you're willing to build the infrastructure. This is a proof of concept that could become a protocol.

### Part 3: The Architecture - Why It's Complicated

Let me explain why we have a Rust TCP proxy sitting between the Python CLI and the Bitwig extension. This sounds like over-engineering. It's not.

Bitwig's RemoteSocket API has a bug. When the extension acts as a TCP server and accepts connections, it can send data but the receive callback never fires. The extension literally cannot hear responses. I spent weeks debugging this, trying different approaches, before discovering that client mode works perfectly - both send and receive function correctly.

So the architecture inverts the connection direction. The Rust proxy listens on two ports. Bitwig connects outward to the proxy as a client. The Python CLI connects to the proxy from the other side. The proxy shuttles messages between them. It's a kludge around a platform bug, but it works reliably.

The Python CLI contains all the domain knowledge. Device resolution, preset search, fuzzy matching, YAML parsing - all Python. The Bitwig extension is a thin layer that receives commands and executes them. The Rust proxy is just plumbing.

Why Python for the CLI? Because search algorithms and text processing are more expressive in Python than Java. Why Java for the extension? Because that's what Bitwig supports. Why Rust for the proxy? Because Rust is excellent for reliable network code, and I didn't want the proxy to ever crash.

### Part 4: Device Resolution - The Fuzzy Search

When you type "nektar piano" in a prompt, how does the system know you mean the Nektar Piano preset and not something else?

The resolver searches in order: presets, base devices, plugins, Kontakt instruments, M-Tron patches. For each category, it uses fuzzy matching with position-weighted scoring. Exact matches score highest. Substring matches at word boundaries score well. Substring matches anywhere score okay. Partial word matches score lowest.

There's randomization on ties. If three presets score identically, the system adds small random jitter so you don't always get the same one. This is intentional - it encourages exploration and prevents the first alphabetical result from always winning.

Device name matches get weighted higher than preset name matches. If you search "Polymer," you probably want the Polymer instrument, not a preset that happens to include "polymer" in its name. The scoring reflects this.

You can override the resolver with hints. If you write `query: "Piano", hint: device`, it will only search base devices, skipping presets. This is useful when names are ambiguous or when you specifically want a base device instead of a preset.

### Part 5: The YAML Format - Design Decisions

The song YAML format evolved through iteration. Early versions were more verbose. Current versions are more implicit.

The `instrument` key means "this is the main sound source, load it first." The `note_fx` key means "these process MIDI before it reaches the instrument." The `fx` key means "these process audio after the instrument." This maps to Bitwig's device chain model.

The `receives` key transforms a track from an instrument track to an audio bus. It creates Audio Receiver devices that pull audio from other tracks. Pre-fader and post-fader options determine whether the receive follows the source track's volume automation.

The `master` track is special. It doesn't create a new track - it adds effects to the master bus that already exists. Every DAW has a master bus. Every mix should have something on it.

The `part` key loads MIDI into the clip launcher. You can use MIDI files directly or ABC notation files that get converted. ABC notation is a text-based music format that's easy to edit and version control. It's how I write the actual notes.

### Part 6: ABC Notation - Why Text Music?

ABC notation comes from traditional folk music. It was designed to be typed on a basic keyboard and printed in newsletters. Letters represent notes - C, D, E, F, G, A, B. Octaves shift with commas and apostrophes. Durations change with numbers and slashes.

For vibe coding, ABC has advantages over MIDI files. It's readable. You can look at `|: C2 E2 G2 | A2 G2 E2 :|` and know it's a simple arpeggio pattern. You can edit it in any text editor. You can version control it meaningfully - git diff shows you which notes changed.

The tool converts ABC to MIDI using abc2midi, then inserts the MIDI into Bitwig's clip launcher. You get the convenience of text notation with the compatibility of MIDI.

The limitation is that ABC notation is designed for melody, not modern electronic production. Complex drum patterns, precisely timed automation, microtonal music - these push against ABC's limitations. For complex parts, write MIDI directly. For simple melodic lines and chord progressions, ABC is faster.

### Part 7: Effects Chains - Common Patterns

Let's talk about why certain effects appear together in the demos.

**Compression after distortion.** Distortion creates harmonics and increases perceived loudness but also increases dynamic range unpredictably. Compression after distortion tames the peaks while keeping the grit.

**Reverb in series.** This sounds wrong until you try it. The first reverb creates initial reflections and room sound. The second reverb diffuses those reflections further, creating depth without obvious echoes. Shoegaze lives here.

**Gate before compressor.** Gates clean up noise during silent passages. Compressors then act on cleaner signal, avoiding pumping artifacts from amplified noise floor.

**EQ before compression vs. after.** EQ before compression means the compressor reacts to the shaped signal. Cut low-mids before compression and the compressor won't pump on bass frequencies. EQ after compression shapes the already-compressed signal without affecting dynamics behavior. Both are valid, depends on intent.

**Tape-Machine on master.** Tape saturation adds subtle harmonic distortion and natural compression. On the master bus, it glues the mix together and adds warmth. But be careful - too much will dull transients and muddy the low end.

### Part 8: Master Bus Philosophy

Every demo includes a master bus. Here's why the effects choices matter.

**EQ-5 or Dynamic EQ.** Visual feedback while mixing. Not for aggressive shaping - that should happen on individual tracks. The master EQ catches problems you missed and provides a final polish. High-pass below 30Hz to remove subsonic garbage. Maybe a gentle high shelf for air. Surgical cuts for resonant problems.

**Compression or Soft Compression.** Glue compression. 2-4 dB of gain reduction maximum. Slow attack to preserve transients, medium release to avoid pumping. The goal is cohesion, not loudness. Aggressive compression on the master destroys dynamics and makes mastering engineers cry.

**Peak Limiter or Hard Clipper.** These do different things. Peak limiters catch transients transparently. Hard clippers chop them off abruptly. For clean genres, limiter. For aggressive genres, clipper. The clipper adds harmonics - that's distortion, intentional distortion.

**What not to do.** Don't put reverb on the master bus unless you're making vaporwave or lo-fi. Don't use heavy compression to make things louder - that's mastering's job. Don't stack limiters thinking more is better. Don't add exciter or widener plugins that make everything sound "better" in isolation but worse in context.

### Part 9: Genre-Specific Production Notes

**Techno and House.** Kick and bass relationship is everything. They share frequency space - one has to move when the other hits. Sidechain compression, EQ carving, or arrangement choices (bass plays between kicks). The hi-hat pattern creates groove through tiny timing variations - swing, humanization, or intentional machine precision.

**Drum and Bass.** The breaks are the composition. Not drums underneath music - drums AS music. Processing breaks involves careful transient work. Too compressed and they lose punch. Too dynamic and they disappear in the mix. The sub bass is separate from everything else - it lives in the 30-80Hz range and should be mono.

**Hip Hop and Trap.** The 808 is both drum and bass. The kick transient hits, then the sustained sub bass carries. This requires careful mixing - the transient needs to cut through, the sustain needs to fill but not overwhelm. Hi-hat patterns define the subgenre more than any other element.

**Rock and Metal.** Guitar tone starts at the amp. No plugin will fix a bad source tone. Double-tracking guitars hard-panned is standard for width. The bass fills the space between kick and guitars - often needs to be distorted more than you'd expect to be audible in a dense mix. Drums in metal require extensive sample replacement or augmentation to achieve modern heaviness.

**Electronic Pop.** Vocals sit on top of everything. The entire mix should be a bed for the vocal. Sidechain compression not just on bass but potentially on multiple elements, creating that pumping modern sound. Synth leads need to be bright but not harsh - the 2-4kHz range is precious real estate.

### Part 10: The Role of Presets

Presets have a reputation problem. "Real" producers make sounds from scratch. "Amateur" producers use presets.

This is snobbery that wastes time.

A preset is a starting point. It encodes decisions made by sound designers who understand synthesis deeply. When you use a preset, you're not cheating - you're standing on the shoulders of experts. The question is what you do next.

Using a preset unmodified and calling it done? That's problematic - not because presets are bad, but because one size fits nobody. Presets are designed to sound impressive in solo. In a mix, they usually need adjustment. The bass preset that sounds huge alone might be too wide and too bright in context. The pad that sounds beautiful alone might conflict with your chord voicing.

The workflow: load preset, evaluate in context, modify to fit. Bitwig's preset browser actually helps here - you can audition presets against your existing arrangement before committing.

### Part 11: Sends vs. Inserts

The demos use both approaches and the distinction matters.

Insert effects go directly in the track's signal chain. The entire signal passes through them. Insert means commitment - the wet/dry mix of a distortion insert determines how much distortion exists, period.

Send effects use buses. Multiple tracks send to one effect instance. The send amount determines each track's contribution. This is efficient (one reverb instead of eight) and coherent (everything shares the same acoustic space).

When to use which?

Compression is almost always an insert. You want to compress this specific signal, not a blend with other signals.

Reverb and delay are often sends. Multiple instruments in the same reverb creates realistic space. Different instruments hitting the same delay creates rhythmic cohesion.

Distortion depends on intent. Subtle saturation can be a send, blending distorted and clean. Aggressive distortion is usually an insert - you want that specific signal destroyed.

The demos show this distinction with the `receives` keyword. A track with receives is a bus. Its effects apply to the mixed signal from multiple sources.

### Part 12: Gain Staging

Here's what actually matters about gain staging, without the pseudoscience.

Digital audio has one hard limit: 0 dBFS. Above that, clipping. Below that, infinite headroom mathematically (practically, noise floor exists around -144 dB in 24-bit).

The goal is to hit that limit exactly once - at the master output, after the final limiter. Everything before that should have headroom. How much? Enough that occasional transients don't clip individual channels.

A practical approach: keep individual track peaks around -12 to -6 dBFS. Keep the mix bus peaking around -6 dBFS before the limiter. Let the limiter catch peaks and bring up the overall level.

Why -12 to -6? Historical convention and plugin design. Many plugins are modeled on analog gear that sounds different at different input levels. Hitting them too hot can cause unintended distortion. Hitting them too soft might miss their sweet spot.

The mixer faders in Bitwig (and most DAWs) are your gain staging tools. If something is too hot, turn down the fader. If it's too quiet in the mix, turn up the fader. This is simpler than it sounds because people overthink it.

### Part 13: Monitoring and Reference

This isn't about gear recommendations. It's about methodology.

Whatever you mix on, learn its lies. Every playback system has a frequency response curve. Your monitors might have a bass bump. Your headphones might have a scooped midrange. Your car might have a subwoofer that adds octaves that don't exist in the recording.

The solution is references. Take a professionally mixed song in your genre and put it in your session. A/B against it constantly. If your bass sounds weak compared to the reference, your bass IS weak - regardless of what your monitors tell you in isolation.

Reference at low volumes. Fletcher-Munson curves mean that at high volumes, bass and treble seem louder relative to midrange. At low volumes, this effect diminishes. If your mix sounds balanced at low volumes, it'll sound balanced anywhere.

Take breaks. Ear fatigue is real and insidious. After an hour of mixing, your perception has shifted. Take fifteen minutes away. Come back and problems that were invisible become obvious.

### Part 14: When to Break the Rules

Every production "rule" is actually a default. Defaults work most of the time. When they don't work, you need to know why they're defaults to know how to break them meaningfully.

"Don't put reverb on bass." Default because reverb creates pitch ambiguity and low-frequency mud. But dub reggae puts reverb on bass constantly and that's the whole point.

"Don't compress the master too hard." Default because mastering should handle that. But if you're making harsh electronic music and the distorted compression IS the aesthetic, compress away.

"Keep bass mono." Default because stereo bass causes phase issues on playback systems. But if the bass is really a sub synth and a separate mid bass, the mid bass can be stereo while the sub stays mono.

The key is intention. Breaking rules by accident creates problems. Breaking rules on purpose creates genre.

### Part 15: The Future of AI in Music Production

We're at the beginning of something. Right now, this tool creates empty arrangements with presets loaded. You still write the notes, design the automation, mix the levels. The AI is doing the scaffolding.

The trajectory points toward more. AI that suggests chord progressions fitting your melody. AI that generates drum patterns from natural language. AI that mixes tracks based on genre conventions. AI that writes entire songs.

I have mixed feelings about that future.

The democratization argument: these tools let people without traditional training make music. Good. Music should be accessible.

The homogenization argument: if everyone uses the same AI with similar prompts, everything sounds the same. Concerning. But this already happened with presets and sample packs - homogenization is a human problem, not a technology problem.

The authenticity argument: is AI-assisted music "real" music? Wrong question. All music uses tools. The question is whether the result moves people. That's independent of how it was made.

My bet is that AI becomes another instrument. Like synthesizers didn't replace acoustic instruments but became their own thing, AI won't replace human composition but will become its own thing. New genres will emerge that are only possible with AI assistance. Other genres will explicitly reject AI in the same way some musicians reject computers entirely.

The interesting question isn't whether AI can make music. It can. The question is what music only AI can make that we'd actually want to hear.

### Part 16: Claude Code Specifically

Claude Code is different from chat-based AI tools. It operates in your filesystem, runs commands, edits files directly. This changes the interaction model.

For this project, Claude Code reads the YAML configuration, has access to the CLI documentation, understands the device resolution system. When I tell it "make a drum and bass track with jungle influences," it can write the YAML, run the CLI command, and set up Bitwig without me specifying every detail.

The key is that Claude Code maintains context. A chat-based tool forgets between sessions. Claude Code has CLAUDE.md - the context document you're reading right now - which persists across interactions. It knows what the project does, what conventions to follow, what patterns work.

This matters for production workflows. Instead of explaining the system every time, I can say "add a reverb bus for the strings section" and Claude Code knows what that means in this project's context. It generates appropriate YAML, uses correct device names, follows established patterns.

The limitation is that Claude Code operates at the text level. It can't hear the music. It doesn't know if the preset sounds good for this context. It can't evaluate whether the mix is balanced. Human ears remain essential. But the scaffolding - creating tracks, loading devices, setting up routing - that's handled.

### Part 17: Practical Session Workflow

Here's how I actually use this system in practice.

Start with genre and vibe. "Atmospheric drum and bass with jazz influences." Write the initial YAML with basic structure - drums, bass, keys, atmosphere, bus routing, master effects.

Run `bitwig project create`. Tracks appear in Bitwig. Devices load. Signal chains establish.

Open Bitwig and start writing. Play the instruments, find melodic ideas, record MIDI. The presets are starting points - tweak them as needed. Adjust the device chains based on what the specific sounds require.

Mix as you go. Don't wait until everything is recorded to start mixing. The mix IS part of the composition for electronic music. How loud the reverb bus is changes the vibe fundamentally.

Export stems for mastering or finish in Bitwig with mastering plugins on the master bus. Depending on destination and how much polish is needed.

The AI part is front-loaded. It builds the studio for this specific song. The human part is everything after - writing, performing, mixing, finishing.

### Part 18: Common Failure Modes

**Too many tracks.** Every track adds complexity. Every track is a mixing decision. Start with fewer tracks than you think you need. Add only when necessary.

**Wrong tempo for genre.** Tempo defines energy. 128 BPM house feels different than 172 BPM jungle. Knowing the right tempo range for your genre prevents structural problems.

**Conflicting effects.** Two competing reverbs create confusion, not depth. Two distortions might fight each other rather than complement. Think about what each effect is doing before stacking.

**No master bus processing.** Running the master bus raw means missing the final glue stage. Even minimal processing - gentle compression and limiting - makes a difference.

**Over-reliance on presets.** Presets are starting points. Using them unmodified means your sound is identical to everyone else using that preset. Modify to fit context.

**Ignoring genre conventions.** You can break rules, but know what rules you're breaking. Putting heavy reverb on trap drums works if you're intentionally making weird trap. If you're trying to make standard trap, it's a mistake.

### Part 19: Final Thoughts on the Project

Groove Link is infrastructure. It's plumbing between Claude Code and Bitwig. The value isn't in the code - it's in what the code enables.

What it enables is natural language music production. Not generated music - scaffolded music. You describe what you want, the system builds the environment, you create within that environment.

This changes who can produce music. Traditional production requires learning a DAW, understanding synthesis, knowing signal flow, remembering preset names. Groove Link compresses that learning curve. You can produce music while learning, rather than learning before producing.

It also changes how experienced producers work. Instead of repetitive setup tasks, you describe the setup and it happens. More time creating, less time clicking.

The demos in this video are invitations. Each prompt is a starting point for your own exploration. Take them, modify them, break them, improve them. The system handles the setup. What you create is yours.

---

## Closing

**[NARRATION - 30 seconds]**

We covered forty song templates across genres from ambient to gabber. We talked about production philosophy, signal flow, mixing decisions, and when to break the rules. This is vibe coding for music production - describing what you want and letting the system build it.

The code is open source. The presets are Bitwig stock. Everything else is your creativity applied to the scaffolding.

Make something.

---

*Groove Link - Natural language music production for Bitwig Studio*
*Built with Claude Code*
