import pathlib
import sys

import librosa
import numpy as np
import sounddevice as sd


def analyse_pitch(audio_path_str):
    # 1. Locate Audio File
    AUDIO_PATH = pathlib.Path(audio_path_str)

    if not AUDIO_PATH.exists():
        sys.exit(f"File not found: {AUDIO_PATH}")

    print(f"Loading  ➜  {AUDIO_PATH.name}")
    wav, sr = librosa.load(AUDIO_PATH, sr=None, mono=True)  # audioread handles MP3, AAC, WAV, FLAC …

    dur = len(wav) / sr
    print(f"Duration  : {dur:.2f} s  |  Sample-rate: {sr} Hz")

    # 2. Pitch-tracking (librosa.pyin)
    LOW_NOTE = 'C2'  # ≈65 Hz
    HIGH_NOTE = 'C6'  # ≈1 kHz

    print("Analyzing pitch…")
    f0, voiced_flag, _ = librosa.pyin(
        wav,
        fmin=librosa.note_to_hz(LOW_NOTE),
        fmax=librosa.note_to_hz(HIGH_NOTE),
        sr=sr
    )
    vf0 = f0[voiced_flag]

    if vf0.size == 0:
        sys.exit("No voiced frames detected. Try a cleaner recording or adjust fmin/fmax.")

    stats = {
        "mean_Hz": float(np.nanmean(vf0)),
        "median_Hz": float(np.nanmedian(vf0)),
        "min_Hz": float(np.nanmin(vf0)),
        "max_Hz": float(np.nanmax(vf0))
    }

    print("\nFundamental-frequency summary:")
    for k, v in stats.items():
        print(f"  {k:<10} : {v:7.1f} Hz")

    # 3. Save a text report next to the audio
    report_path = AUDIO_PATH.with_suffix(".pitch.txt")
    report = {}
    with open(report_path, "w", encoding="utf-8") as f:
        report['File'] = AUDIO_PATH.name
        f.write(f"File: {AUDIO_PATH.name}\n")
        report['Duration'] = dur
        f.write(f"Duration: {dur:.2f} s\n")
        report['Sample-rate'] = sr
        f.write(f"Sample-rate: {sr} Hz\n")
        for k, v in stats.items():
            report[k] = f"{v} Hz"
            f.write(f"{k:<10}: {v:7.1f} Hz\n")

    print(f"\n✅ Pitch report saved ➜  {report_path}")
    return report_path
