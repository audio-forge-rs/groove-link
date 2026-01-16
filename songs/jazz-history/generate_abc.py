#!/usr/bin/env python3
"""Generate ABC files for Jazz History with guaranteed correct bar counts."""

ERAS = [
    {"name": "New Orleans", "bars": 48, "tempo": 96, "key": "Bb"},
    {"name": "Stride", "bars": 48, "tempo": 112, "key": "F"},
    {"name": "Swing", "bars": 64, "tempo": 144, "key": "Bb"},
    {"name": "Bebop", "bars": 64, "tempo": 200, "key": "Bb"},
    {"name": "Cool", "bars": 48, "tempo": 80, "key": "C"},
    {"name": "Hard Bop", "bars": 48, "tempo": 130, "key": "Fm"},
    {"name": "Modal", "bars": 48, "tempo": 68, "key": "Dm"},
    {"name": "Free", "bars": 32, "tempo": 160, "key": "Ab"},
    {"name": "Fusion", "bars": 48, "tempo": 108, "key": "Em"},
    {"name": "Contemporary", "bars": 48, "tempo": 100, "key": "C"},
]

TOTAL_BARS = sum(e["bars"] for e in ERAS)  # 496

# Pattern library - each pattern is exactly 8 bars
# Format: list of 8 bar strings (each bar is 8 eighth notes worth)
PATTERNS = {
    "piano": {
        "New Orleans": ["[B,DF]2[B,DF]2[B,DF]2[B,DF]2"] * 8,
        "Stride": ["F,,2[A,CF]2C,,2[A,CF]2"] * 8,
        "Swing": ["z2[BDF]2z2[BDF]2"] * 8,
        "Bebop": ["z4[BDF]4"] * 8,
        "Cool": ["[E,G,B,D]8"] * 8,
        "Hard Bop": ["z2[FAc]2z2[FAc]2"] * 8,
        "Modal": ["[D,G,C]8"] * 8,
        "Free": ["[A,CE]4z4"] * 8,
        "Fusion": ["z2[EGB]2z[EGB]3"] * 8,
        "Contemporary": ["[C,E,G,B,]4[D,F,A,C]4"] * 8,
    },
    "bass": {
        "New Orleans": ["B,,4F,4"] * 8,
        "Stride": ["F,,4C,4"] * 8,
        "Swing": ["B,,2D,2F,2A,2"] * 8,
        "Bebop": ["B,,2D,2F,2A,2"] * 8,
        "Cool": ["C,2E,2G,2B,2"] * 8,
        "Hard Bop": ["F,2A,2C2E2"] * 8,
        "Modal": ["D,8"] * 8,
        "Free": ["A,,4z4"] * 8,
        "Fusion": ["E,2z2E,2z2"] * 8,
        "Contemporary": ["C,2E,2G,2B,2"] * 8,
    },
    "trumpet": {
        "New Orleans": ["B,2D2F2B2"] * 8,
        "Stride": ["F2A2c2f2"] * 8,
        "Swing": ["B2d2f2b2"] * 8,
        "Bebop": ["BcdBfgaf"] * 8,
        "Cool": ["E8"] * 8,
        "Hard Bop": ["F2A2c2f2"] * 8,
        "Modal": ["D8"] * 8,
        "Free": ["A,2z2c2z2"] * 8,
        "Fusion": ["E2zE2zG2"] * 8,
        "Contemporary": ["C2E2G2c2"] * 8,
    },
    "trombone": {
        "New Orleans": ["B,,4D,4"] * 8,
        "Stride": ["F,4A,4"] * 8,
        "Swing": ["B,2D2F2B2"] * 8,
        "Bebop": ["B,CDB,FGAF"] * 8,
        "Cool": ["C,8"] * 8,
        "Hard Bop": ["F,2A,2C2F2"] * 8,
        "Modal": ["D,8"] * 8,
        "Free": ["A,,4z4"] * 8,
        "Fusion": ["E,2zE,2zG,2"] * 8,
        "Contemporary": ["C,2E,2G,2C2"] * 8,
    },
    "clarinet": {
        "New Orleans": ["d2f2b2d'2"] * 8,
        "Stride": ["c2e2a2c'2"] * 8,
        "Swing": ["d2f2b2d'2"] * 8,
        "Bebop": ["defBfgab"] * 8,
        "Cool": ["G8"] * 8,
        "Hard Bop": ["c2e2a2c'2"] * 8,
        "Modal": ["A8"] * 8,
        "Free": ["c2z2e2z2"] * 8,
        "Fusion": ["G2zG2zB2"] * 8,
        "Contemporary": ["E2G2B2e2"] * 8,
    },
    "drum-kick": {
        "New Orleans": ["C4C4"] * 8,
        "Stride": ["C4z4"] * 8,
        "Swing": ["C4z4"] * 8,
        "Bebop": ["z8"] * 8,
        "Cool": ["C8"] * 8,
        "Hard Bop": ["C4z4"] * 8,
        "Modal": ["C8"] * 8,
        "Free": ["C4z4"] * 8,
        "Fusion": ["C4z2C2"] * 8,
        "Contemporary": ["C4z4"] * 8,
    },
    "drum-snare": {
        "New Orleans": ["z4C4"] * 8,
        "Stride": ["z4C4"] * 8,
        "Swing": ["z4z2C2"] * 8,
        "Bebop": ["z8"] * 8,
        "Cool": ["z8"] * 8,
        "Hard Bop": ["z4C4"] * 8,
        "Modal": ["z8"] * 8,
        "Free": ["z4C4"] * 8,
        "Fusion": ["z4C4"] * 8,
        "Contemporary": ["z4z2C2"] * 8,
    },
    "drum-ride": {
        "New Orleans": ["C8"] * 8,
        "Stride": ["C2C2C2C2"] * 8,
        "Swing": ["C2zCzCC2"] * 8,
        "Bebop": ["C2zCzCC2"] * 8,
        "Cool": ["C2C2C2C2"] * 8,
        "Hard Bop": ["C2zCzCC2"] * 8,
        "Modal": ["C2zCzCC2"] * 8,
        "Free": ["C2C2z2C2"] * 8,
        "Fusion": ["CCCCCCCC"] * 8,
        "Contemporary": ["C2zCzCC2"] * 8,
    },
}


def generate_era(instrument: str, era: dict) -> str:
    """Generate ABC for one era with exact bar count."""
    name = era["name"]
    bars = era["bars"]
    tempo = era["tempo"]
    key = era["key"]

    pattern = PATTERNS[instrument][name]

    lines = []
    lines.append(f"%%")
    lines.append(f"%% {name.upper()} ({bars} bars, {tempo} BPM)")
    lines.append(f"%%")
    lines.append(f"Q:1/4={tempo}")

    # Handle key changes for bass/trombone (bass clef)
    if instrument in ["bass", "trombone"]:
        lines.append(f"K:{key} bass")
    else:
        lines.append(f"K:{key}")

    # Generate bars using the 8-bar pattern
    bar_count = 0
    while bar_count < bars:
        row_bars = []
        for i in range(8):  # 8 bars per row
            if bar_count < bars:
                pattern_idx = bar_count % len(pattern)
                row_bars.append(pattern[pattern_idx])
                bar_count += 1
        lines.append("|".join(row_bars) + "|")

    return "\n".join(lines)


def generate_instrument(instrument: str) -> str:
    """Generate complete ABC file for one instrument."""
    # Determine clef
    clef = "bass" if instrument in ["bass", "trombone"] else ""
    first_key = ERAS[0]["key"]
    if clef:
        first_key += " " + clef

    # Use C for drums
    if instrument.startswith("drum"):
        first_key = "C"

    header = f"""X:1
T:Jazz History - {instrument.replace('-', ' ').title()}
M:4/4
L:1/8
K:{first_key}"""

    sections = [header]
    for era in ERAS:
        sections.append(generate_era(instrument, era))

    return "\n".join(sections)


def count_bars(abc_content: str) -> int:
    """Count bars in ABC content."""
    return abc_content.count("|")


def main():
    import os

    os.makedirs(".", exist_ok=True)

    instruments = ["piano", "bass", "trumpet", "trombone", "clarinet",
                   "drum-kick", "drum-snare", "drum-ride"]

    all_valid = True

    for instrument in instruments:
        abc = generate_instrument(instrument)
        bars = count_bars(abc)

        if bars != TOTAL_BARS:
            print(f"ERROR: {instrument}.abc has {bars} bars, expected {TOTAL_BARS}")
            all_valid = False
        else:
            print(f"OK: {instrument}.abc = {bars} bars")
            with open(f"{instrument}.abc", "w") as f:
                f.write(abc)

    if all_valid:
        print(f"\nAll {len(instruments)} files generated with {TOTAL_BARS} bars each.")
    else:
        print(f"\nERROR: Some files have incorrect bar counts!")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
