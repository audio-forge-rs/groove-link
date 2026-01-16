#!/usr/bin/env python3
"""
Generate ABC backing tracks for Blue Wind Blew - RICK RUBIN EDITION
108 bars at 133 BPM - Country heartbreak ballad in Bb

This isn't mechanical backing - this is MUSIC.
- Walking bass with chromatic approaches
- Fingerpicked guitar arpeggios
- Rhodes-style piano comping with swing
- Brush kit drums with dynamics
"""

TEMPO = 133
KEY = "Bb"
TIME = "4/4"
TOTAL_BARS = 108

# Structure: 4-bar intro + 13 × 8-bar sections
INTRO_BARS = 4
NUM_SECTIONS = 13

# Chord progression per 8-bar section
# |: Bb | Bb | Eb | Eb | Bb | Bb | F | F :|
CHORDS = ["Bb", "Bb", "Eb", "Eb", "Bb", "Bb", "F", "F"]


def generate_bass():
    """
    Walking bass - the heartbeat of the song.
    Root-fifth is boring. We walk with chromatic approaches,
    leading tones, and rhythmic variation.
    """
    # Bass patterns per chord - multiple variations
    patterns = {
        "Bb": [
            "B,,2F,,2B,,2F,,2",           # Basic
            "B,,2D,2F,2D,2",               # Walk up
            "B,,4F,,2A,,2",                # Longer root
            "B,,2F,,2D,2B,,2",             # Down walk
        ],
        "Eb": [
            "E,,2B,,2E,2B,,2",             # Basic
            "E,,2G,,2B,,2G,,2",            # Walk up
            "E,,4B,,2D,2",                 # Approach to Bb
            "E,,2B,,2G,,2E,,2",            # Down walk
        ],
        "Bb_to_Eb": [
            "B,,2D,2^D,2E,2",              # Chromatic approach up
        ],
        "Eb_to_Bb": [
            "E,,2D,2C,2B,,2",              # Chromatic approach down
        ],
        "Bb_to_F": [
            "B,,2A,,2^G,,2F,,2",           # Chromatic approach down
        ],
        "F": [
            "F,,2C,2F,2C,2",               # Basic
            "F,,2A,,2C,2A,,2",             # Walk up
            "F,,4C,2E,2",                  # Approach to Bb
            "F,,2C,2A,,2F,,2",             # Down walk
        ],
        "F_to_Bb": [
            "F,,2A,,2=B,,2B,,2",           # Leading tone resolution
        ],
    }

    import random
    random.seed(42)  # Reproducible but varied

    lines = []

    # 4-bar intro - sparse, building
    lines.append("z8 | z8 | B,,4z4 | B,,2F,,2B,,2z2 |")

    # 13 sections with variation
    for section in range(NUM_SECTIONS):
        section_bars = []

        for i, chord in enumerate(CHORDS):
            # Determine if we need a transition pattern
            if i == 1 and chord == "Bb":  # Bb before Eb
                bar = random.choice(patterns["Bb_to_Eb"])
            elif i == 3 and chord == "Eb":  # Eb before Bb
                bar = random.choice(patterns["Eb_to_Bb"])
            elif i == 5 and chord == "Bb":  # Bb before F
                bar = random.choice(patterns["Bb_to_F"])
            elif i == 7 and chord == "F":  # F before next Bb
                bar = patterns["F_to_Bb"][0]
            else:
                bar = random.choice(patterns[chord])

            section_bars.append(bar)

        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_guitar():
    """
    Fingerpicked arpeggios - the soul of country.
    Each pattern is exactly 8 eighth notes.
    """
    # Verified 8-eighth patterns: each note is 1 eighth
    patterns = {
        "Bb": [
            "B,,D,F,D,B,,D,F,D,",           # 8 notes up-down
            "D,F,B,F,D,F,B,F,",             # Mid-range bounce
            "B,,B,,D,D,F,F,D,D,",           # Pairs
            "F,D,B,,D,F,D,B,,D,",           # Down-up
        ],
        "Eb": [
            "E,,G,B,G,E,,G,B,G,",           # 8 notes up-down
            "G,B,E,B,G,B,E,B,",             # Mid-range bounce
            "E,,E,,G,G,B,B,G,G,",           # Pairs
            "B,G,E,,G,B,G,E,,G,",           # Down-up
        ],
        "F": [
            "F,,A,C,A,F,,A,C,A,",           # 8 notes up-down
            "A,C,F,C,A,C,F,C,",             # Mid-range bounce
            "F,,F,,A,A,C,C,A,A,",           # Pairs
            "C,A,F,,A,C,A,F,,A,",           # Down-up
        ],
    }

    import random
    random.seed(43)

    lines = []

    # 4-bar intro (8 eighths per bar)
    lines.append("B,,D,F,D,B,,D,F,D, | D,F,B,F,D,F,B,F, | B,,D,F,D,B,,D,F,D, | F,D,B,,D,F,D,B,,D, |")

    for _ in range(NUM_SECTIONS):
        section_bars = []
        for chord in CHORDS:
            bar = random.choice(patterns[chord])
            section_bars.append(bar)
        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_piano():
    """
    Rhodes-style comping - sparse but meaningful.
    Not every beat - leave space for the vocals to breathe.
    Swing feel with anticipations.
    """
    # Voicings and rhythms - jazz-influenced country
    patterns = {
        "Bb": [
            "[B,,D,F,]4 z2[B,DF]2",          # Hit and answer
            "z2[B,DF]2 [B,,D,F,]4",          # Anticipated
            "[B,,D,F,B,]6 z2",               # Long chord
            "z4 [B,DF]4",                    # Backbeat only
        ],
        "Eb": [
            "[E,,G,,B,,]4 z2[E,GB,]2",
            "z2[E,GB,]2 [E,,G,,B,,]4",
            "[E,,G,,B,,E,]6 z2",
            "z4 [E,GB,]4",
        ],
        "F": [
            "[F,,A,,C,]4 z2[F,A,C]2",
            "z2[F,A,C]2 [F,,A,,C,]4",
            "[F,,A,,C,F,]6 z2",
            "z4 [F,A,C]4",
        ],
    }

    import random
    random.seed(44)

    lines = []

    # 4-bar intro - piano enters gently
    lines.append("z8 | z8 | z4 [B,DF]4 | [B,,D,F,]4 z2[B,DF]2 |")

    for section in range(NUM_SECTIONS):
        section_bars = []
        for chord in CHORDS:
            bar = random.choice(patterns[chord])
            section_bars.append(bar)
        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_drums_kick():
    """
    Kick drum - not mechanical 4-on-floor.
    Country feel with emphasis on 1, occasional 3.
    Space is musical.
    """
    patterns = [
        "C,4z4",              # Just the 1
        "C,4z2C,2",           # 1 and 3
        "C,2z2C,4",           # Syncopated
        "C,4C,4",             # Both strong beats
    ]

    import random
    random.seed(45)

    lines = []

    # Intro - minimal
    lines.append("z8 | z8 | C,4z4 | C,4z4 |")

    for section in range(NUM_SECTIONS):
        section_bars = []
        for i in range(8):
            # More minimal on verses (odd sections), fuller on choruses
            if section % 2 == 0:
                bar = random.choice(patterns[:2])
            else:
                bar = random.choice(patterns)
            section_bars.append(bar)
        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_drums_snare():
    """
    Snare/brush - the backbeat.
    2 and 4, but with ghost notes and variation.
    """
    patterns = [
        "z2E2z2E2",           # Classic 2 and 4 (8 eighths)
        "z2E,Ez2E2",          # Ghost on 2 (8 eighths)
        "z2E2z2E,E",          # Ghost lead-out (8 eighths)
        "z2E,E,z2E2",         # Double ghost (8 eighths)
    ]

    import random
    random.seed(46)

    lines = []

    # Intro - brushes enter
    lines.append("z8 | z8 | z2E2z4 | z2E2z2E2 |")

    for section in range(NUM_SECTIONS):
        section_bars = []
        for _ in range(8):
            bar = random.choice(patterns)
            section_bars.append(bar)
        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_drums_hihat():
    """
    Hi-hat/ride - the pulse.
    Eighth notes but with accents and occasional opens.
    """
    patterns = [
        "^F^F^F^F^F^F^F^F",           # Straight eighths
        "^F^f^F^f^F^f^F^f",           # Accented
        "^F^F^f^F^F^F^f^F",           # Varied accents
        "^F^F^F^G^F^F^F^F",           # Open on &3
    ]

    import random
    random.seed(47)

    lines = []

    # Intro - ride bell enters
    lines.append("z8 | ^F2z2^F2z2 | ^F^F^F^F^F^F^F^F | ^F^F^F^F^F^F^F^F |")

    for section in range(NUM_SECTIONS):
        section_bars = []
        for i in range(8):
            # Vary between patterns
            bar = patterns[i % len(patterns)]
            section_bars.append(bar)
        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def write_abc(filename, title, body):
    """Write ABC file with header."""
    header = f"""X:1
T:{title}
M:{TIME}
L:1/8
Q:1/4={TEMPO}
K:{KEY}"""

    content = header + "\n" + body + "\n"

    with open(filename, 'w') as f:
        f.write(content)

    bar_count = content.count('|')
    status = "✓" if bar_count == TOTAL_BARS else "✗"
    print(f"{status} {filename}: {bar_count} bars (expected {TOTAL_BARS})")
    return bar_count == TOTAL_BARS


def main():
    import os
    base_dir = "/Users/bedwards/groove-link/songs/bard/abc"
    os.makedirs(base_dir, exist_ok=True)

    parts = [
        ("bass.abc", "Blue Wind Blew - Walking Bass", generate_bass()),
        ("guitar.abc", "Blue Wind Blew - Fingerpicked Guitar", generate_guitar()),
        ("piano.abc", "Blue Wind Blew - Rhodes Comp", generate_piano()),
        ("drum-kick.abc", "Blue Wind Blew - Kick", generate_drums_kick()),
        ("drum-snare.abc", "Blue Wind Blew - Brush Snare", generate_drums_snare()),
        ("drum-hihat.abc", "Blue Wind Blew - Ride", generate_drums_hihat()),
    ]

    print(f"🎸 Generating {TOTAL_BARS}-bar backing tracks - RICK RUBIN EDITION\n")

    all_ok = True
    for filename, title, body in parts:
        path = os.path.join(base_dir, filename)
        ok = write_abc(path, title, body)
        if not ok:
            all_ok = False

    print()
    if all_ok:
        print(f"✓ All tracks ready to VIBE ({TOTAL_BARS} bars each)")
    else:
        print("✗ Bar count mismatch - fix it!")

    return all_ok


if __name__ == "__main__":
    main()
