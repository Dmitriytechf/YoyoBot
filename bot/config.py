import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TG_TOKEN_YOYO')
CHAT_ID = os.getenv('CHAT_ID')
LOTR_API = os.getenv('LOTR_API')
BRENT_API = os.getenv('BRENT_API')
GOLD_API = os.getenv('GOLD_API')
WEATHER_API = os.getenv('WEATHER_API')
