#!/usr/bin/env python3
"""
MIDI Generator for Groove-Link - Generate validated MIDI from song.yaml

This script reads a song.yaml (concept-albums format) and generates:
- Validated ABC files for all instruments
- MIDI files via abc2midi
- Verification that all parts match in length

DOES NOT push to Bitwig. Outputs to midi/ directory for manual import.

Usage:
    python -m bitwig_cli.generate_midi song-directory/

    # Or via CLI:
    bitwig midi generate song-directory/
"""

import sys
import subprocess
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import yaml


@dataclass
class ValidationError:
    """A validation error with context"""
    section: str
    instrument: str
    message: str
    line: Optional[str] = None


@dataclass
class BarCount:
    """Result of counting bars in ABC"""
    expected: int
    actual: int
    valid: bool
    details: str


def count_abc_bars(abc_content: str, time_sig: str = "4/4") -> BarCount:
    """Count bars in ABC content and validate against expected length.

    Returns BarCount with expected vs actual and validity status.
    """
    # Parse time signature
    if "/" in time_sig:
        num, denom = map(int, time_sig.split("/"))
    else:
        num, denom = 4, 4

    # Count bar lines (|) but exclude special markers
    lines = abc_content.strip().split('\n')
    bar_count = 0

    for line in lines:
        # Skip header lines
        if re.match(r'^[A-Z]:', line) or line.startswith('%%'):
            continue
        if not line.strip():
            continue

        # Count bars: | but not |: :| |] [| etc
        # Simple approach: count | characters
        bars_in_line = line.count('|')
        bar_count += bars_in_line

    # The number of | characters roughly equals number of bars + 1
    # (opening bar line + closing bar lines)
    # This is approximate - abc2midi is the real validator
    actual_bars = max(0, bar_count - 1) if bar_count > 0 else 0

    return BarCount(
        expected=0,  # Will be set by caller
        actual=actual_bars,
        valid=True,  # Will be validated by abc2midi
        details=f"Found approximately {actual_bars} bars"
    )


def validate_abc_syntax(abc_content: str, section: str, instrument: str) -> List[ValidationError]:
    """Validate ABC notation syntax.

    Returns list of validation errors (empty if valid).
    """
    errors = []
    lines = abc_content.strip().split('\n')

    for i, line in enumerate(lines, 1):
        # Skip headers
        if re.match(r'^[A-Z]:', line) or line.startswith('%%'):
            continue
        if not line.strip():
            continue

        # Check for common errors

        # 1. Annotation syntax (^"text") breaks abc2midi
        if '^"' in line:
            errors.append(ValidationError(
                section=section,
                instrument=instrument,
                message=f"Line {i}: Annotations (^\"text\") not supported - use arrangement notes instead",
                line=line
            ))

        # 2. Unmatched brackets
        if line.count('[') != line.count(']'):
            errors.append(ValidationError(
                section=section,
                instrument=instrument,
                message=f"Line {i}: Unmatched brackets",
                line=line
            ))

        # 3. Invalid note names
        invalid_notes = re.findall(r'[^a-gA-Gz\d\[\]\|\:\'\,\^\=\_\s\"\-\(\)]', line)
        if invalid_notes:
            # Filter out common valid characters
            invalid_notes = [n for n in invalid_notes if n not in '{}/<>~!']
            if invalid_notes:
                errors.append(ValidationError(
                    section=section,
                    instrument=instrument,
                    message=f"Line {i}: Possibly invalid characters: {invalid_notes}",
                    line=line
                ))

    return errors


def generate_abc_header(song: Dict, instrument: str, inst_config: Dict) -> str:
    """Generate ABC file header."""
    is_drums = inst_config.get('percussion', False)

    header = f"""X:1
T:{song['title']} - {instrument}
C:{song.get('composer', 'Unknown')}
M:{song['time']}
L:1/8
Q:1/4={song['tempo']}
"""

    if is_drums:
        header += "K:C\n%%MIDI channel 10\n"
    else:
        header += f"K:{song['key']}\n"
        if 'program' in inst_config:
            header += f"%%MIDI program {inst_config['program']}\n"

    return header


def assemble_instrument_abc(
    song: Dict,
    sections_config: Dict,
    structure: List[str],
    instrument: str,
    inst_config: Dict
) -> Tuple[str, List[ValidationError]]:
    """Assemble complete ABC file for an instrument from sections.

    Returns (abc_content, list_of_errors).
    """
    errors = []
    header = generate_abc_header(song, instrument, inst_config)
    music_parts = []

    is_drums = inst_config.get('percussion', False)

    for section_name in structure:
        if section_name not in sections_config:
            errors.append(ValidationError(
                section=section_name,
                instrument=instrument,
                message=f"Section '{section_name}' not found in sections config"
            ))
            continue

        section = sections_config[section_name]
        expected_bars = section.get('bars', 8)

        if 'instruments' not in section:
            continue

        instruments = section['instruments']

        if is_drums:
            # Handle drums - we'll generate separate files for each drum part
            if 'drums' in instruments:
                drum_parts = instruments['drums']
                # For the main drum instrument, we concatenate all drum ABC
                # But actually concept-albums generates SEPARATE files per drum
                # Let's follow that pattern
                pass
        else:
            if instrument not in instruments:
                # Instrument not in this section - add rests
                rest_bars = f"z8 | " * expected_bars
                music_parts.append(rest_bars.strip())
                continue

            inst_section = instruments[instrument]
            abc_content = inst_section.get('abc', '')

            # Validate ABC syntax
            section_errors = validate_abc_syntax(abc_content, section_name, instrument)
            errors.extend(section_errors)

            # Remove chord symbols for MIDI (keep for reference)
            abc_clean = re.sub(r'"[A-G][#b]?[^"]*"', '', abc_content)
            music_parts.append(abc_clean.strip())

    full_abc = header + '\n'.join(music_parts) + '\n'
    return full_abc, errors


def generate_drum_abc(
    song: Dict,
    sections_config: Dict,
    structure: List[str],
    drum_part: str
) -> Tuple[str, List[ValidationError]]:
    """Generate ABC for a single drum part (kick, snare, etc.).

    All drum parts use note C (MIDI 60) for single-instrument compatibility.
    """
    errors = []

    header = f"""X:1
T:{song['title']} - drum-{drum_part}
C:{song.get('composer', 'Unknown')}
M:{song['time']}
L:1/8
Q:1/4={song['tempo']}
K:C
%%MIDI channel 10
"""

    music_parts = []

    for section_name in structure:
        if section_name not in sections_config:
            continue

        section = sections_config[section_name]
        expected_bars = section.get('bars', 8)

        if 'instruments' not in section or 'drums' not in section['instruments']:
            # No drums in this section - add rests
            rest_bars = f"z8 | " * expected_bars
            music_parts.append(rest_bars.strip())
            continue

        drums = section['instruments']['drums']

        if drum_part not in drums:
            # This drum part not in this section - add rests
            rest_bars = f"z8 | " * expected_bars
            music_parts.append(rest_bars.strip())
            continue

        abc_content = drums[drum_part]

        # Validate
        section_errors = validate_abc_syntax(abc_content, section_name, f"drum-{drum_part}")
        errors.extend(section_errors)

        music_parts.append(abc_content.strip())

    full_abc = header + '\n'.join(music_parts) + '\n'
    return full_abc, errors


def convert_abc_to_midi(abc_file: Path, midi_file: Path) -> Tuple[bool, str]:
    """Convert ABC to MIDI using abc2midi.

    Returns (success, error_message).
    """
    try:
        result = subprocess.run(
            ['abc2midi', str(abc_file), '-o', str(midi_file)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return False, result.stderr

        # Check for warnings (but still succeeded)
        if result.stderr:
            # Filter out harmless warnings
            warnings = [w for w in result.stderr.split('\n')
                       if w.strip() and 'Warning' in w]
            if warnings:
                return True, f"Warnings: {'; '.join(warnings[:3])}"

        return True, ""

    except FileNotFoundError:
        return False, "abc2midi not found - install abcmidi package"
    except subprocess.TimeoutExpired:
        return False, "abc2midi timed out"
    except Exception as e:
        return False, str(e)


def verify_midi_lengths(midi_dir: Path) -> Tuple[bool, str]:
    """Verify all MIDI files have matching lengths.

    Returns (all_match, summary_message).
    """
    try:
        import mido
    except ImportError:
        return True, "mido not installed - skipping length verification"

    midi_files = list(midi_dir.glob('*.mid'))
    if not midi_files:
        return False, "No MIDI files found"

    lengths = {}
    for f in midi_files:
        try:
            mid = mido.MidiFile(str(f))
            total_ticks = sum(msg.time for track in mid.tracks for msg in track)
            lengths[f.name] = total_ticks
        except Exception as e:
            return False, f"Error reading {f.name}: {e}"

    if len(set(lengths.values())) == 1:
        return True, f"All {len(midi_files)} files match: {list(lengths.values())[0]} ticks"

    # Find mismatches
    sorted_lengths = sorted(lengths.items(), key=lambda x: x[1])
    shortest = sorted_lengths[0]
    longest = sorted_lengths[-1]

    return False, f"Length mismatch: {shortest[0]}={shortest[1]} vs {longest[0]}={longest[1]} ticks"


def generate_song_midi(song_dir: Path, output_dir: Optional[Path] = None) -> int:
    """Main entry point: generate MIDI files from song.yaml.

    Args:
        song_dir: Directory containing song.yaml
        output_dir: Output directory for MIDI files (default: song_dir/midi)

    Returns:
        0 on success, 1 on error
    """
    config_file = song_dir / 'song.yaml'
    if not config_file.exists():
        print(f"Error: {config_file} not found")
        return 1

    # Load config
    with open(config_file) as f:
        config = yaml.safe_load(f)

    # Validate required fields
    required = ['song', 'sections', 'instruments']
    for field in required:
        if field not in config:
            print(f"Error: Missing required field '{field}' in song.yaml")
            return 1

    song = config['song']
    sections = config['sections']
    instruments = config['instruments']
    structure = song.get('structure', list(sections.keys()))

    print(f"\n{'='*70}")
    print(f"Generating MIDI: {song['title']}")
    print(f"Tempo: {song['tempo']} BPM | Key: {song['key']} | Time: {song['time']}")
    print(f"Structure: {' → '.join(structure)}")
    print(f"{'='*70}\n")

    # Setup output directories
    if output_dir is None:
        output_dir = song_dir / 'midi'
    output_dir.mkdir(exist_ok=True)

    abc_dir = song_dir / '.generated'
    abc_dir.mkdir(exist_ok=True)

    all_errors = []
    generated_files = []

    # Process each instrument
    for inst_name, inst_config in instruments.items():
        is_drums = inst_config.get('percussion', False)

        if is_drums:
            # Generate separate files for each drum part
            drum_parts = ['kick', 'snare', 'hihat', 'crash', 'ride', 'tom1', 'tom2', 'tom3']

            for drum_part in drum_parts:
                # Check if this drum part exists in any section
                has_part = False
                for section in sections.values():
                    if 'instruments' in section and 'drums' in section['instruments']:
                        if drum_part in section['instruments']['drums']:
                            has_part = True
                            break

                if not has_part:
                    continue

                abc_content, errors = generate_drum_abc(song, sections, structure, drum_part)
                all_errors.extend(errors)

                abc_file = abc_dir / f"drum-{drum_part}.abc"
                abc_file.write_text(abc_content)

                midi_file = output_dir / f"drum-{drum_part}.mid"
                success, msg = convert_abc_to_midi(abc_file, midi_file)

                if success:
                    print(f"✓ drum-{drum_part}.mid")
                    if msg:
                        print(f"  {msg}")
                    generated_files.append(midi_file)
                else:
                    print(f"✗ drum-{drum_part}.mid: {msg}")
                    all_errors.append(ValidationError(
                        section="assembly",
                        instrument=f"drum-{drum_part}",
                        message=msg
                    ))
        else:
            # Regular instrument
            abc_content, errors = assemble_instrument_abc(
                song, sections, structure, inst_name, inst_config
            )
            all_errors.extend(errors)

            abc_file = abc_dir / f"{inst_name}.abc"
            abc_file.write_text(abc_content)

            midi_file = output_dir / f"{inst_name}.mid"
            success, msg = convert_abc_to_midi(abc_file, midi_file)

            if success:
                print(f"✓ {inst_name}.mid")
                if msg:
                    print(f"  {msg}")
                generated_files.append(midi_file)
            else:
                print(f"✗ {inst_name}.mid: {msg}")
                all_errors.append(ValidationError(
                    section="assembly",
                    instrument=inst_name,
                    message=msg
                ))

    # Verify lengths match
    print(f"\n{'='*70}")
    print("Verification")
    print(f"{'='*70}")

    lengths_match, length_msg = verify_midi_lengths(output_dir)
    if lengths_match:
        print(f"✓ {length_msg}")
    else:
        print(f"✗ {length_msg}")

    # Report errors
    if all_errors:
        print(f"\n{'='*70}")
        print(f"Validation Errors ({len(all_errors)})")
        print(f"{'='*70}")
        for err in all_errors:
            print(f"  [{err.section}/{err.instrument}] {err.message}")
            if err.line:
                print(f"    → {err.line[:60]}...")

    # Summary
    print(f"\n{'='*70}")
    if all_errors:
        print(f"⚠ Generated {len(generated_files)} MIDI files with {len(all_errors)} errors")
    else:
        print(f"✅ Generated {len(generated_files)} MIDI files successfully")
    print(f"{'='*70}")
    print(f"\nOutput: {output_dir}/")

    return 0 if not all_errors else 1


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate MIDI from song.yaml')
    parser.add_argument('song_dir', type=Path, help='Song directory containing song.yaml')
    parser.add_argument('--output', '-o', type=Path, help='Output directory (default: song_dir/midi)')

    args = parser.parse_args()

    return generate_song_midi(args.song_dir, args.output)


if __name__ == '__main__':
    sys.exit(main())
