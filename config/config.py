import os
from dotenv import load_dotenv

load_dotenv()

# Mantém compatibilidade com possíveis nomes antigos de variável.
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("GROP_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"
