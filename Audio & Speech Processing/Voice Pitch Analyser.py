import librosa
import numpy as np
import pathlib
import sounddevice as sd
import sys

# 1. Locate Audio File
AUDIO_PATH = pathlib.Path(r"Audio.mp3")

if not AUDIO_PATH.exists():
    sys.exit(f"File not found: {AUDIO_PATH}")

print(f"Loading  ➜  {AUDIO_PATH.name}")
wav, sr = librosa.load(AUDIO_PATH, sr=None, mono=True)  # audioread handles MP3, AAC, WAV, FLAC …

dur = len(wav) / sr
print(f"Duration  : {dur:.2f} s  |  Sample-rate: {sr} Hz")

# 2. Play it back so you can confirm it sounds right
print("Playing… (Ctrl-C to skip)")
try:
    sd.play(wav, sr)
    sd.wait()
except KeyboardInterrupt:
    sd.stop()

# 3. Pitch-tracking (librosa.pyin)
LOW_NOTE = 'C2'   # ≈65 Hz
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

# 4. Save a text report next to the audio
report_path = AUDIO_PATH.with_suffix(".pitch.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(f"File: {AUDIO_PATH.name}\n")
    f.write(f"Duration: {dur:.2f} s\n")
    for k, v in stats.items():
        f.write(f"{k:<10}: {v:7.1f} Hz\n")

print(f"\n✅ Pitch report saved ➜  {report_path}")
