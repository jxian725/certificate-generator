from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class Settings:
    DB_URL = os.getenv("DB_URL")  # e.g. postgresql+psycopg2://certuser:pass@localhost:5432/certdb
    OBS_BUCKET = os.getenv("OBS_BUCKET", "")
    OBS_ENDPOINT = os.getenv("OBS_ENDPOINT", "")
    OBS_AK = os.getenv("OBS_AK", "")
    OBS_SK = os.getenv("OBS_SK", "")
    EVENT_NAME = os.getenv("EVENT_NAME", "Huawei Developer Competition 2025")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

settings = Settings()
