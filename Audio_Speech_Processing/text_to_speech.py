"""Text-to-speech with optional file output for a web interface."""

from pathlib import Path

import pyttsx3


def text_to_speech(text: str = "Text to speech function invoked.",
                   is_male: int = 0, rate: int = 200,
                   output_path: str | None = None) -> str | None:
    """Use 0 for male and 1 for female; actual voices depend on the OS."""
    if not text.strip():
        raise ValueError("Text must not be empty")
    engine = pyttsx3.init()
    try:
        voices = engine.getProperty("voices")
        if voices:
            desired = "female" if is_male else "male"
            matching = [
                v for v in voices
                if desired in (str(getattr(v, "gender", "")) + " " +
                               str(getattr(v, "name", ""))).lower()
            ]
            chosen = (matching[0] if matching else
                      voices[min(1 if is_male else 0, len(voices) - 1)])
            engine.setProperty("voice", chosen.id)
        engine.setProperty("rate", rate)
        if output_path:
            target = str(Path(output_path))
            engine.save_to_file(text, target)
        else:
            engine.say(text)
        engine.runAndWait()
        return output_path
    finally:
        engine.stop()
