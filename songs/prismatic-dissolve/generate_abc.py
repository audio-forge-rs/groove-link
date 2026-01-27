#!/usr/bin/env python3
"""
PRISMATIC DISSOLVE - A 6-minute psychedelic jam
96 BPM, E minor, 144 bars

Not loops - a journey. Each section evolves.
Swirling arpeggios, hypnotic bass, cosmic pads, liquid drums.
"""

import random

TEMPO = 96
KEY = "Em"
TIME = "4/4"
TOTAL_BARS = 144  # 6 minutes at 96 BPM

# Structure: 18 sections of 8 bars each
# Each section has a different vibe - building, releasing, floating
SECTIONS = [
    {"name": "intro", "intensity": 0.2, "bars": 8},
    {"name": "emerge", "intensity": 0.3, "bars": 8},
    {"name": "pulse1", "intensity": 0.5, "bars": 8},
    {"name": "float1", "intensity": 0.4, "bars": 8},
    {"name": "build1", "intensity": 0.6, "bars": 8},
    {"name": "peak1", "intensity": 0.8, "bars": 8},
    {"name": "dissolve1", "intensity": 0.5, "bars": 8},
    {"name": "drift", "intensity": 0.3, "bars": 8},
    {"name": "rebirth", "intensity": 0.4, "bars": 8},
    {"name": "pulse2", "intensity": 0.6, "bars": 8},
    {"name": "ascend", "intensity": 0.7, "bars": 8},
    {"name": "peak2", "intensity": 0.9, "bars": 8},
    {"name": "kaleidoscope", "intensity": 1.0, "bars": 8},
    {"name": "shatter", "intensity": 0.7, "bars": 8},
    {"name": "float2", "intensity": 0.5, "bars": 8},
    {"name": "memories", "intensity": 0.4, "bars": 8},
    {"name": "fade", "intensity": 0.2, "bars": 8},
    {"name": "void", "intensity": 0.1, "bars": 8},
]

# Chord progression - modal, dreamy
# Em - Am - C - Bm (i - iv - VI - v)
CHORDS = ["Em", "Am", "C", "Bm"]


def generate_arp():
    """
    Swirling arpeggios - the kaleidoscope.
    Different patterns per section, never static.
    """
    # Base patterns for each chord - multiple variations
    patterns = {
        "Em": [
            "E,G,B,G,E,G,B,G,",           # Basic up-down
            "B,G,E,G,B,G,E,G,",           # Inverted
            "E,B,G,B,E,B,G,B,",           # Skip pattern
            "G,E,B,E,G,E,B,E,",           # Mid-rooted
            "E,G,E,B,G,B,G,E,",           # Wave
            "B,E,G,E,B,G,E,G,",           # Cascade
        ],
        "Am": [
            "A,,C,E,C,A,,C,E,C,",
            "E,C,A,,C,E,C,A,,C,",
            "A,,E,C,E,A,,E,C,E,",
            "C,A,,E,A,,C,E,A,,E,",
            "A,,C,A,,E,C,E,C,A,,",
            "E,A,,C,A,,E,C,A,,C,",
        ],
        "C": [
            "C,E,G,E,C,E,G,E,",
            "G,E,C,E,G,E,C,E,",
            "C,G,E,G,C,G,E,G,",
            "E,C,G,C,E,G,C,G,",
            "C,E,C,G,E,G,E,C,",
            "G,C,E,C,G,E,C,E,",
        ],
        "Bm": [
            "B,,D,^F,D,B,,D,^F,D,",
            "^F,D,B,,D,^F,D,B,,D,",
            "B,,^F,D,^F,B,,^F,D,^F,",
            "D,B,,^F,B,,D,^F,B,,^F,",
            "B,,D,B,,^F,D,^F,D,B,,",
            "^F,B,,D,B,,^F,D,B,,D,",
        ],
    }

    # Sparse patterns for low intensity
    sparse = {
        "Em": "E,2z2G,2z2",
        "Am": "A,,2z2C,2z2",
        "C": "C,2z2E,2z2",
        "Bm": "B,,2z2D,2z2",
    }

    random.seed(100)
    lines = []

    for section in SECTIONS:
        section_bars = []
        intensity = section["intensity"]

        for bar_num in range(section["bars"]):
            chord = CHORDS[bar_num % 4]

            if intensity < 0.3:
                # Very sparse
                bar = sparse[chord]
            elif intensity < 0.5:
                # Mix of sparse and pattern
                if random.random() < 0.5:
                    bar = sparse[chord]
                else:
                    bar = random.choice(patterns[chord][:2])
            else:
                # Full patterns, more variation at higher intensity
                num_patterns = min(6, int(intensity * 6) + 1)
                bar = random.choice(patterns[chord][:num_patterns])

            section_bars.append(bar)

        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_bass():
    """
    Hypnotic bass - the anchor.
    Long notes that breathe, occasional movement.
    """
    patterns = {
        "Em": [
            "E,,8",                        # Whole note
            "E,,4E,4",                     # Octave pulse
            "E,,4z2E,,2",                  # Breath
            "E,,2z2E,,2E,2",               # Walk up
            "E,,2E,2E,,2z2",               # Bounce
        ],
        "Am": [
            "A,,8",
            "A,,4A,4",
            "A,,4z2A,,2",
            "A,,2z2A,,2A,2",
            "A,,2A,2A,,2z2",
        ],
        "C": [
            "C,8",
            "C,4C4",
            "C,4z2C,2",
            "C,2z2C,2C2",
            "C,2C2C,2z2",
        ],
        "Bm": [
            "B,,8",
            "B,,4B,4",
            "B,,4z2B,,2",
            "B,,2z2B,,2B,2",
            "B,,2B,2B,,2z2",
        ],
    }

    random.seed(101)
    lines = []

    for section in SECTIONS:
        section_bars = []
        intensity = section["intensity"]

        for bar_num in range(section["bars"]):
            chord = CHORDS[bar_num % 4]

            if intensity < 0.2:
                # Mostly silence with occasional hits
                if random.random() < 0.3:
                    bar = patterns[chord][0]
                else:
                    bar = "z8"
            elif intensity < 0.5:
                # Simple whole notes
                bar = random.choice(patterns[chord][:2])
            else:
                # More movement
                bar = random.choice(patterns[chord])

            section_bars.append(bar)

        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_pad():
    """
    Cosmic pads - the atmosphere.
    Long sustained chords, slow evolution.
    """
    chords = {
        "Em": "[E,G,B,]8",
        "Am": "[A,,C,E,]8",
        "C": "[C,E,G,]8",
        "Bm": "[B,,D,^F,]8",
    }

    # Extended voicings for peaks
    extended = {
        "Em": "[E,,B,,E,G,B,e]8",
        "Am": "[A,,E,A,C,E,a]8",
        "C": "[C,G,C,E,G,c]8",
        "Bm": "[B,,^F,B,D,^F,b]8",
    }

    random.seed(102)
    lines = []

    for section in SECTIONS:
        section_bars = []
        intensity = section["intensity"]

        for bar_num in range(section["bars"]):
            chord = CHORDS[bar_num % 4]

            if intensity < 0.3:
                # Mostly silence
                if random.random() < 0.3:
                    bar = chords[chord]
                else:
                    bar = "z8"
            elif intensity < 0.7:
                # Simple chords
                bar = chords[chord]
            else:
                # Extended voicings
                bar = extended[chord]

            section_bars.append(bar)

        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_lead():
    """
    Liquid lead - the consciousness.
    Melodic fragments that appear and disappear.
    """
    # Pentatonic phrases in E minor (E G A B D)
    phrases = [
        "e2d2B2G2",           # Descend
        "G2A2B2d2",           # Ascend
        "e4z2d2",             # Long-short
        "B2A2G2E2",           # Low descend
        "E2G2A2B2",           # Low ascend
        "d2e2d2B2",           # Turn
        "G2B2d2e2",           # Leap up
        "e2B2G2E2",           # Cascade down
        "z2e2d2B2",           # Late entry
        "e2z2d2z2",           # Sparse high
        "B4A4",               # Held notes
        "G2A2B2z2",           # Unfinished
    ]

    random.seed(103)
    lines = []

    for section in SECTIONS:
        section_bars = []
        intensity = section["intensity"]

        for bar_num in range(section["bars"]):
            if intensity < 0.4:
                # Mostly silent, occasional phrase
                if random.random() < 0.15:
                    bar = random.choice(phrases[-4:])  # Sparse phrases
                else:
                    bar = "z8"
            elif intensity < 0.7:
                # Some phrases
                if random.random() < 0.4:
                    bar = random.choice(phrases)
                else:
                    bar = "z8"
            else:
                # Active lead
                if random.random() < 0.7:
                    bar = random.choice(phrases)
                else:
                    bar = "z8"

            section_bars.append(bar)

        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_kick():
    """
    Deep kick - the heartbeat.
    Four on the floor when intense, sparse when floating.
    """
    patterns = [
        "C,4z4",              # Just beat 1
        "C,4z2C,2",           # 1 and 3
        "C,2z2C,2z2",         # 1 and 3 short
        "C,2C,2C,2C,2",       # Four on floor
        "C,2z2C,4",           # Syncopated
    ]

    random.seed(104)
    lines = []

    for section in SECTIONS:
        section_bars = []
        intensity = section["intensity"]

        for _ in range(section["bars"]):
            if intensity < 0.2:
                bar = "z8"
            elif intensity < 0.4:
                bar = patterns[0] if random.random() < 0.5 else "z8"
            elif intensity < 0.6:
                bar = random.choice(patterns[:2])
            elif intensity < 0.8:
                bar = random.choice(patterns[:4])
            else:
                bar = random.choice(patterns)

            section_bars.append(bar)

        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_snare():
    """
    Snare/clap - the pulse.
    2 and 4 when grooving, sparse in floaty sections.
    """
    patterns = [
        "z2E2z2E2",           # Classic 2 and 4 (8)
        "z4E4",               # Just 3 (8)
        "z2E4z2",             # 2 only (8)
        "z2E2z2E,E",          # 2 and 4 with ghost (8)
        "zE,E2z2E2",          # Ghost before 2 (8)
    ]

    random.seed(105)
    lines = []

    for section in SECTIONS:
        section_bars = []
        intensity = section["intensity"]

        for _ in range(section["bars"]):
            if intensity < 0.3:
                bar = "z8"
            elif intensity < 0.5:
                bar = patterns[1] if random.random() < 0.4 else "z8"
            elif intensity < 0.7:
                bar = random.choice(patterns[:2])
            else:
                bar = random.choice(patterns)

            section_bars.append(bar)

        lines.append(" | ".join(section_bars) + " |")

    return "\n".join(lines)


def generate_hats():
    """
    Hats/shaker - the shimmer.
    Sixteenths when intense, sparse otherwise.
    """
    patterns = [
        "^F^F^F^F^F^F^F^F",           # Eighths
        "^F2^F2^F2^F2",               # Quarters
        "^f^F^f^F^f^F^f^F",           # Accented eighths
        "z2^F2z2^F2",                 # Sparse
        "^F4z4",                      # Half only
        "^F^f^F^f^F^f^F^f",           # Driving
    ]

    random.seed(106)
    lines = []

    for section in SECTIONS:
        section_bars = []
        intensity = section["intensity"]

        for _ in range(section["bars"]):
            if intensity < 0.2:
                bar = "z8"
            elif intensity < 0.4:
                bar = patterns[4] if random.random() < 0.4 else "z8"
            elif intensity < 0.6:
                bar = random.choice(patterns[3:5])
            elif intensity < 0.8:
                bar = random.choice(patterns[:4])
            else:
                bar = random.choice(patterns)

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
    base_dir = "/Users/bedwards/groove-link/songs/prismatic-dissolve/abc"
    os.makedirs(base_dir, exist_ok=True)

    parts = [
        ("arp.abc", "Prismatic Dissolve - Arpeggio", generate_arp()),
        ("bass.abc", "Prismatic Dissolve - Bass", generate_bass()),
        ("pad.abc", "Prismatic Dissolve - Pad", generate_pad()),
        ("lead.abc", "Prismatic Dissolve - Lead", generate_lead()),
        ("kick.abc", "Prismatic Dissolve - Kick", generate_kick()),
        ("snare.abc", "Prismatic Dissolve - Snare", generate_snare()),
        ("hats.abc", "Prismatic Dissolve - Hats", generate_hats()),
    ]

    print(f"🌈 PRISMATIC DISSOLVE - {TOTAL_BARS} bars at {TEMPO} BPM\n")

    all_ok = True
    for filename, title, body in parts:
        path = os.path.join(base_dir, filename)
        ok = write_abc(path, title, body)
        if not ok:
            all_ok = False

    print()
    if all_ok:
        print("✓ Ready to dissolve into the prismatic void")
    else:
        print("✗ Bar count issues - fix before proceeding")

    return all_ok


if __name__ == "__main__":
    main()
