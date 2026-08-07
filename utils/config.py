from dotenv import load_dotenv
import os

# This line reads the .env file and loads its values
# into the environment, so os.getenv() can find them.
load_dotenv()

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Assistant")