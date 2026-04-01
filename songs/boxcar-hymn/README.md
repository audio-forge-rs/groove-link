## Boxcar Hymn — Overview

**104 BPM | Bb Major / G Minor | 4/4 | ~9 minutes**

A slow-rolling train beat folk song. Think Townes Van Zandt meets Wilco's quieter moments — lots of space, instruments drifting in and out like passengers boarding and leaving. You're the engine (guitar, banjo, mandolin, vocals). Everything else is scenery passing by the window.

---

### Reload Instructions

1. Bitwig → Settings → Controllers
2. Disable the RPC Controller, wait 2 sec, re-enable it
3. Wait for "RPC v0.5.13" popup
4. Tell me and I'll insert the remaining 18 MIDI clips

---

### Track Layout (top to bottom in Bitwig)

```
 #  Track            Role
──  ───────────────  ─────────────────────────────────────
 1  drums            Modified train beat. Kick/snare/hats.
                     Rimshot swaps in for ghost notes.
                     Half-time in bridges, driving in solo.

 2  congas           Enters V2. Syncopated slaps, gaps.
 3  tambourine       Quarters in chorus, 8ths when it builds.
 4  shaker           Steady 8ths in bridge/chorus only.
 5  clap             Backbeat (2 & 4) in choruses only.
 6  washboard        Scrubby rhythm in bridges. Folk grit.
 7  bicycle          Rare single dings. A wink, not a part.

 8  bass_root        ★ The anchor. Whole-note roots, never busy.
 9  bass_walk        Walking quarter notes in choruses/solo.
10  bass_fill        Transition runs between sections. Sparse.

11  piano_chords     Beat-1 block chords. Barely there in verses.
12  piano_arp        Arpeggiated chords in choruses. Gentle.
13  piano_high       High bell-like accents. Bridges/solo only.

14  synth_pad        Warm sustained wash. Background glow.
15  synth_arp        Phase-4 through arpeggiator. Electronic pulse.
16  synth_texture    Aparillo ambient texture. Bridges/solo.

17  hammond_chords   Gospel organ sustains. Choruses + bridges.
18  hammond_swell    Volume swells underneath. Late entry.
19  hammond_riff     Short blues stabs. "Yeah!" moments.

20  steel_melody     ★ Weeping country lines. Intro + interludes.
21  steel_chord      Dyad pads. Warm shimmer in choruses.
22  steel_slide      Single bending notes. Grace note feel.

23  mtron_strings    Mellotron strings wash. Chorus/bridge color.
24  mtron_flute      Mellotron flute melody fragments. Bridges.
25  mtron_choir      Mellotron choir. Only appears at the peak
                     (Chorus 5 last 8 bars). The big moment.

26  fiddle_melody    ★ Pentatonic lines. V1, V2, solo, Ch5.
27  fiddle_drone     Open-string sustains. Bridges. Dark bed.
28  fiddle_chop      Rhythmic chop on 2 & 4. Chorus energy.

29  harp_melody      Bluesy harmonica lines. Choruses/solo.
30  harp_chords      Harmonica dyad pads. Bridges.
31  harp_wail        Bending wails. Very sparse. Gut-punch.

32  room             Reverb bus (piano, steel, fiddle, harp).
33  master           Peak limiter.
```

---

### The Arc

| Section | Bars | Feel | Who's playing |
|---------|------|------|---------------|
| **Intro** | 1-8 | Spare. Rimshot + pedal hat. Steel cries. | drums, bass, steel |
| **Verse 1** | 9-24 | Train beat starts. Piano appears. | + piano, fiddle melody |
| **Chorus 1** | 25-32 | First lift. Tambourine, clap, organ enter. | + tamb, clap, hammond, harp, mtron strings |
| **Interlude 1** | 33-40 | Breathe. Steel melody + synth pad. | drums light, bass, steel, pad |
| **Verse 2** | 41-56 | Fuller. Congas, synth arp, fiddle return. | + congas, synth_arp, fiddle |
| **Chorus 2** | 57-64 | Building. Walking bass, fiddle chop. | + bass_walk, fiddle_chop, steel_chord |
| **Bridge 1** | 65-80 | Dark turn. Half-time drums. Gm → Cm. Washboard, shaker, drone. | half-time, washboard, shaker, fiddle_drone, mtron_flute |
| **Chorus 3** | 81-88 | Release back to major. | full band minus extras |
| **Interlude 2** | 89-96 | Drums drop out. Bass alone. Bicycle ding. | bass, bicycle, steel, synth_arp |
| **Verse 3** | 97-112 | Darker (Cm subs). Hammond takes piano's role. Harp wail enters. | drums, bass, hammond, shaker, harp_wail |
| **Chorus 4** | 113-128 | Extended 16-bar. Everything building. | nearly full band |
| **Solo** | 129-144 | Driving drums. Fiddle + harp + steel trade solos over verse changes. | fiddle_melody, harp_melody, steel_melody, bass_walk |
| **Bridge 2** | 145-160 | Half-time again. Mellotron strings return. Washboard. | half-time, mtron_strings, mtron_flute, washboard |
| **Verse 4** | 161-176 | Rhythmic variation (Bb-Gm alternating). Sparser. | drums, bass, hammond_swell, steel sparse |
| **Chorus 5** | 177-192 | **THE BIG ONE.** 16 bars. Everything plays. Mellotron choir enters for the last 8. | ALL tracks |
| **Interlude 3** | 193-200 | Unwinding. Light drums, steel, pad. | drums light, bass, steel, pad |
| **Verse 5** | 201-216 | Final verse. Stripped back to basics. | drums, bass, piano, fiddle, mtron_flute |
| **Outro** | 217-236 | 4-bar cycle fading. Steel and bass last to leave. One final bicycle ding. | fading everything, steel, bass, bicycle |

---

### For You (playing on top)

- **Acoustic guitar/banjo** — you're the rhythmic backbone, especially in verses where the backing is very thin
- **Electric guitar/mandolin** — lead melody, counter-melody, call-and-response with steel/fiddle/harp
- **Vocals** — the song is built around you; the backing instruments deliberately leave the mid-range open
- **Chord chart** is in `songs/boxcar-hymn/chords.txt` — every bar numbered

The ★ tracks (bass_root, steel_melody, fiddle_melody) are the ones most likely to interact with your playing. Everything else is atmosphere.
