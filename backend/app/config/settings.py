import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    FRONTEND_ORIGIN = os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5173",
    )