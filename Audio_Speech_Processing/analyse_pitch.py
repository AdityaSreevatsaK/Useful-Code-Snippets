"""Estimate fundamental frequency from an audio recording."""

from pathlib import Path

import librosa
import numpy as np


def analyse_pitch(audio_path_str: str) -> dict:
    """Return JSON-compatible pitch statistics and write a sibling text report."""
    source = Path(audio_path_str)
    if not source.is_file():
        raise FileNotFoundError(source)
    samples, sample_rate = librosa.load(str(source), sr=None, mono=True)
    if not len(samples) or sample_rate <= 0:
        raise ValueError("Audio recording is empty")
    frequency, is_voiced, _ = librosa.pyin(
        samples, fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C6"), sr=sample_rate,
    )
    voiced = frequency[is_voiced] if is_voiced is not None else np.array([])
    voiced = voiced[np.isfinite(voiced)]
    if not len(voiced):
        raise ValueError("No voiced frames detected")
    result = {
        "mean_Hz": float(np.mean(voiced)),
        "median_Hz": float(np.median(voiced)),
        "min_Hz": float(np.min(voiced)),
        "max_Hz": float(np.max(voiced)),
        "duration_seconds": float(len(samples) / sample_rate),
        "sample_rate_Hz": int(sample_rate),
    }
    report_path = source.with_suffix(".pitch.txt")
    report_path.write_text(
        "\n".join(f"{key}: {value}" for key, value in result.items()) + "\n",
        encoding="utf-8",
    )
    return result
