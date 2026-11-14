"""Cross-platform text-to-speech, including reliable Linux WAV export."""

from pathlib import Path
import shutil
import subprocess
import sys

import pyttsx3


def text_to_speech(text: str = "Text to speech function invoked.",
                   is_male: int = 0, rate: int = 200,
                   output_path: str | None = None) -> str | None:
    """Speak locally or save WAV audio for browser playback.

    Voice gender is best-effort, depending on the installed speech engine.
    0 = male, 1 = female.
    """
    if not text.strip():
        raise ValueError("Text must not be empty")
    if len(text) > 5000:
        raise ValueError("Text must not exceed 5,000 characters")
    if not 50 <= rate <= 300:
        raise ValueError("Speech rate must be between 50 and 300 wpm")
    if is_male not in (0, 1, False, True):
        raise ValueError("Voice selection must be male or female")

    # pyttsx3's Linux eSpeak backend may not save files despite reporting success.
    # Use the CLI's supported -w option for reliable WAV export instead.
    if output_path and sys.platform.startswith("linux"):
        binary = shutil.which("espeak-ng") or shutil.which("espeak")
        if not binary:
            raise RuntimeError("Speech export requires espeak-ng or espeak on Linux")
        target = Path(output_path)
        voice = "en+m3" if not is_male else "en+f3"
        subprocess.run(
            [binary, "-v", voice, "-s", str(rate), "-w", str(target), "--", text],
            capture_output=True, text=True, check=True, timeout=60,
        )
        if not target.is_file() or target.stat().st_size <= 44:
            raise RuntimeError("The speech engine did not generate a valid WAV file")
        return str(target)

    engine = pyttsx3.init()
    try:
        voices = engine.getProperty("voices")
        if voices:
            desired = "male" if not is_male else "female"
            matching = [
                voice for voice in voices
                if desired in (
                    str(getattr(voice, "gender", "")) + " " +
                    str(getattr(voice, "name", ""))
                ).lower()
            ]
            chosen = matching[0] if matching else voices[min(int(bool(is_male)), len(voices) - 1)]
            engine.setProperty("voice", chosen.id)
        engine.setProperty("rate", rate)
        if output_path:
            engine.save_to_file(text, output_path)
        else:
            engine.say(text)
        engine.runAndWait()
        if output_path:
            target = Path(output_path)
            if not target.is_file() or not target.stat().st_size:
                raise RuntimeError("The speech engine did not generate an audio file")
            return str(target)
        return None
    finally:
        engine.stop()
