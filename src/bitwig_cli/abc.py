"""ABC notation to MIDI conversion and verification.

Converts ABC notation files to MIDI using abc2midi and verifies
that all MIDI files have matching durations.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass
class ABCConversionResult:
    """Result of ABC to MIDI conversion."""

    abc_file: Path
    midi_file: Path | None
    success: bool
    error: str | None = None
    warnings: list[str] | None = None


@dataclass
class MIDILengthInfo:
    """Length information for a MIDI file."""

    file_path: Path
    ticks: int
    bars: float  # In 4/4 time
    bpm: float


@dataclass
class LengthVerificationResult:
    """Result of verifying MIDI lengths match."""

    files: list[MIDILengthInfo]
    all_match: bool
    shortest: MIDILengthInfo | None
    longest: MIDILengthInfo | None


def abc_to_midi(
    abc_file: Path,
    output_file: Path | None = None,
    timeout: float = 10.0,
) -> ABCConversionResult:
    """Convert an ABC file to MIDI using abc2midi.

    Args:
        abc_file: Path to the ABC notation file
        output_file: Path for output MIDI file (default: same name with .mid)
        timeout: Timeout in seconds for abc2midi

    Returns:
        ABCConversionResult with success status and any errors/warnings
    """
    if not abc_file.exists():
        return ABCConversionResult(
            abc_file=abc_file,
            midi_file=None,
            success=False,
            error=f"ABC file not found: {abc_file}",
        )

    if output_file is None:
        output_file = abc_file.with_suffix(".mid")

    try:
        result = subprocess.run(
            ["abc2midi", str(abc_file), "-o", str(output_file)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        # Parse warnings from stderr
        warnings = []
        has_error = False
        for line in result.stderr.strip().split("\n"):
            if line:
                if "Error" in line:
                    has_error = True
                    warnings.append(line)
                elif "Bar" in line and "time units" in line:
                    # Bar length mismatch warning
                    warnings.append(line)
                elif line.strip():
                    warnings.append(line)

        if has_error:
            return ABCConversionResult(
                abc_file=abc_file,
                midi_file=None,
                success=False,
                error="; ".join(warnings) if warnings else "abc2midi error",
                warnings=warnings,
            )

        if not output_file.exists():
            return ABCConversionResult(
                abc_file=abc_file,
                midi_file=None,
                success=False,
                error="abc2midi did not create output file",
            )

        return ABCConversionResult(
            abc_file=abc_file,
            midi_file=output_file,
            success=True,
            warnings=warnings if warnings else None,
        )

    except subprocess.TimeoutExpired:
        return ABCConversionResult(
            abc_file=abc_file,
            midi_file=None,
            success=False,
            error="abc2midi timed out",
        )
    except FileNotFoundError:
        return ABCConversionResult(
            abc_file=abc_file,
            midi_file=None,
            success=False,
            error="abc2midi not found - please install abcmidi package",
        )
    except Exception as e:
        return ABCConversionResult(
            abc_file=abc_file,
            midi_file=None,
            success=False,
            error=str(e),
        )


def count_bars(abc_content: str) -> int:
    """Count the number of bars in ABC notation content.

    Handles multi-bar lines correctly.
    For multi-voice files (e.g. drums), counts only the first voice.
    """
    lines = abc_content.split("\n")
    music_lines = []
    in_first_voice = True

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip headers, lyrics, comments
        if line.startswith(("X:", "T:", "C:", "M:", "L:", "Q:", "K:", "w:", "%")):
            if not line.startswith("%%"):  # Keep %%MIDI lines for context
                continue

        # Detect voice changes - only count first voice
        if line.startswith("V:"):
            in_first_voice = line.startswith("V:1")
            continue

        if line.startswith("%%MIDI"):
            continue

        # Only add lines from first voice (or single-voice files)
        if in_first_voice:
            music_lines.append(line)

    music_content = "\n".join(music_lines)

    # Count pipe symbols
    bar_count = 0
    bar_count += music_content.count("|")

    # Subtract special markers that aren't bar lines
    bar_count -= music_content.count("|:")
    bar_count -= music_content.count(":|")
    bar_count -= music_content.count("|]")

    # The final bar before |] counts as 1 bar
    if "|]" in music_content:
        bar_count += 1

    return bar_count


def get_midi_length(midi_file: Path) -> MIDILengthInfo | None:
    """Get length information for a MIDI file.

    Requires mido package. Returns None if mido not available or file invalid.
    """
    try:
        import mido
    except ImportError:
        return None

    try:
        mid = mido.MidiFile(midi_file)

        # Get tempo
        tempo = 500000  # default (120 BPM)
        for track in mid.tracks:
            for msg in track:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
                    break

        # Get total length in ticks
        total_ticks = 0
        for track in mid.tracks:
            track_ticks = sum(msg.time for msg in track)
            total_ticks = max(total_ticks, track_ticks)

        bpm = 60000000 / tempo
        tpb = mid.ticks_per_beat

        # Calculate bars in 4/4 time
        beats = total_ticks / tpb
        bars = beats / 4

        return MIDILengthInfo(
            file_path=midi_file,
            ticks=total_ticks,
            bars=bars,
            bpm=bpm,
        )

    except Exception:
        return None


def verify_midi_lengths(midi_files: list[Path]) -> LengthVerificationResult:
    """Verify that all MIDI files have the same duration.

    Args:
        midi_files: List of MIDI file paths to verify

    Returns:
        LengthVerificationResult with file info and match status
    """
    files_info: list[MIDILengthInfo] = []

    for midi_file in midi_files:
        info = get_midi_length(midi_file)
        if info:
            files_info.append(info)

    if not files_info:
        return LengthVerificationResult(
            files=[],
            all_match=True,
            shortest=None,
            longest=None,
        )

    # Find min and max
    shortest = min(files_info, key=lambda x: x.ticks)
    longest = max(files_info, key=lambda x: x.ticks)

    all_match = shortest.ticks == longest.ticks

    return LengthVerificationResult(
        files=files_info,
        all_match=all_match,
        shortest=shortest,
        longest=longest,
    )


def find_abc_files(directory: Path) -> Iterator[Path]:
    """Find all ABC files in a directory."""
    if directory.is_file() and directory.suffix == ".abc":
        yield directory
    elif directory.is_dir():
        yield from directory.glob("*.abc")
        yield from directory.glob("**/*.abc")
