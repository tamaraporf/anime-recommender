import os
from dotenv import load_dotenv

load_dotenv()

GROP_API_KEY = os.getenv("GROP_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"

