import os

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model Configuration
MODEL = os.getenv("MODEL", "deepseek/deepseek-chat")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# App Configuration
APP_TITLE = "AI Chatbot"
APP_VERSION = "1.0.0"

# Vercel Configuration
REQUEST_TIMEOUT = 25  # seconds (Vercel limit is 30s)