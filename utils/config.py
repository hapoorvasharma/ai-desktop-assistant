from dotenv import load_dotenv
import os

load_dotenv()

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Assistant")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")