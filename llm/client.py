from google import genai
from google.genai import types
import json
from utils.config import GEMINI_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are a command interpreter for a desktop assistant. Your only job is to
read what the user said and convert it into a JSON array of action objects
describing what to do. You must reply with ONLY the JSON array — no
explanation, no markdown formatting, no extra text.

Each action object must have this shape:
{"action": "<action_name>", "target": "<target_value>"}

If the user asks for multiple things in one sentence (e.g. "open notepad
and open chrome"), return multiple objects in the array, in the order
they should happen. If there's only one thing to do, still return an
array containing just that one object.

Valid action_name values are:
- open_app
- close_app
- restart_app
- open_folder
- search_apps
- create_folder
- delete_file
- search_google
- open_website
- add_favorite
- show_favorites
- show_history
- unknown

If the user's request doesn't match any known action, reply with:
[{"action": "unknown", "target": ""}]

Examples:
User: "can you please open notepad for me"
Reply: [{"action": "open_app", "target": "notepad"}]

User: "open notepad and open chrome"
Reply: [{"action": "open_app", "target": "notepad"}, {"action": "open_app", "target": "chrome"}]

User: "search google for cute cats"
Reply: [{"action": "search_google", "target": "cute cats"}]
"""


def interpret_command(user_message: str) -> list:
    """
    Sends the user's message to Gemini and returns a list of structured
    action dictionaries describing what to do.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
        )

        raw_text = response.text.strip()
        parsed = json.loads(raw_text)

        if isinstance(parsed, dict):
            parsed = [parsed]

        logger.info(f"Interpreted '{user_message}' as: {parsed}")
        return parsed

    except json.JSONDecodeError as e:
        logger.error(f"Gemini reply wasn't valid JSON: {e}")
        return [{"action": "unknown", "target": ""}]
    except Exception as e:
        logger.error(f"Failed to interpret command: {e}")
        return [{"action": "unknown", "target": ""}]