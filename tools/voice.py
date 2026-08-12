import pyttsx3
import speech_recognition as sr
from utils.logger import get_logger

logger = get_logger(__name__)


class Voice:
    """
    Handles voice input (speech-to-text) and voice output (text-to-speech).
    """

    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def speak(self, text: str) -> None:
        """
        Speaks the given text out loud.
        """
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            logger.info(f"Spoke: {text}")
        except Exception as e:
            logger.error(f"Failed to speak: {e}")

    def listen(self) -> str:
        """
        Listens through the microphone and returns recognized text.
        Returns an empty string if nothing could be understood.
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening for voice input...")
                audio = self.recognizer.listen(source)

            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized speech: '{text}'")
            return text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error during listening: {e}")
            return ""