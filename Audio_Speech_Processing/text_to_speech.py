import pyttsx3


def text_to_speech(text: str = "Text to speech function invoked.", is_male: int = False, rate: int = 200):
    """
        Description:
            Convert text to speech using the pyttsx3 library.

        Args:
            text (str, optional): The text to be converted to speech. Defaults to "Text to speech function invoked.".
            is_male (int, optional): Flag to select the voice gender. 0 for male, 1 for female. Defaults to False (0).
            rate (int, optional): The speech rate (words per minute). Defaults to 200.

        Returns:
            None
    """
    engine = pyttsx3.init()
    voices = engine.getProperty(name='voices')  # Get available voices
    voice_type = 0 if is_male == 1 else 1
    engine.setProperty(name='voice', value=voices[voice_type].id)  # Select voice (0: Male, 1: Female)
    engine.setProperty(name='rate', value=rate)  # Set speech rate
    engine.say(text=text)
    engine.runAndWait()
