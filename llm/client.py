from google import genai
from utils.config import GEMINI_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(user_message: str) -> str:
    """
    Sends a message to Gemini and returns its text reply.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_message,
        )
        logger.info(f"Gemini replied to: '{user_message}'")
        return response.text
    except Exception as e:
        logger.error(f"Failed to get response from Gemini: {e}")
        return "Sorry, I couldn't reach Gemini right now."