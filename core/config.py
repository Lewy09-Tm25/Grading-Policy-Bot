import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if it exists)
# This prevents you from hardcoding your API key into the script.
load_dotenv()

# --- API Configuration ---
# Ensure the API key is retrieved safely. The engine will use this later.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file or environment variables.")

# --- Model Selection ---
# You can easily swap this out for 'gpt-4o-mini' if you want to save costs,
# or a newer model string as they are released by OpenAI.
MODEL_NAME = "gpt-5.4"

# --- File Paths ---
# We use relative paths to ensure the code works regardless of where it is executed.
# This assumes the 'data' folder is at the same level as the 'core' folder.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "grading_policy.md")