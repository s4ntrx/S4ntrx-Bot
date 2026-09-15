import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration. Values come from environment variables so that
    no secret ever lives in source control."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is not set. Copy .env.example to .env and fill it in."
        )

    # Database: defaults to local SQLite for development.
    # For the multi-user deployment, set DATABASE_URL to a Postgres/Supabase URI.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 's4ntrx.db')}"
    )

    # AI provider: "knowledge" (default, no external dependency, always works)
    # or "ollama" (requires a local Ollama server — see README before enabling).
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "knowledge")
    OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session / cookie hardening
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    WTF_CSRF_TIME_LIMIT = None  # tokens valid for the whole session


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
