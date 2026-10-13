import os


class Settings:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
        f"/{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FRONTEND_ORIGIN = os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5173",
    )

    ADMIN_SEED_ENABLED = os.getenv(
        "ADMIN_SEED_ENABLED",
        "false",
    ).strip().lower() in {"1", "true", "yes", "on"}
    ADMIN_SEED_FULL_NAME = os.getenv("ADMIN_SEED_FULL_NAME")
    ADMIN_SEED_EMAIL = os.getenv("ADMIN_SEED_EMAIL")
    ADMIN_SEED_PASSWORD = os.getenv("ADMIN_SEED_PASSWORD")
