"""F4: .env + yaml config loader"""
from functools import lru_cache
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
# LangSmith vars os.environ mein chahiye hote hain, isliye load_dotenv bhi
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    DATABASE_URL: str
    GROQ_API_KEY: str
    TELEGRAM_TOKEN: str = ""
    LLM_MODEL: str = "llama-3.3-70b-versatile"


@lru_cache
def get_settings() -> Settings:
    return Settings()


def _load_yaml(name: str) -> dict:
    with open(BASE_DIR / "config" / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache
def get_business_profile() -> dict:
    return _load_yaml("business_profile.yaml")


@lru_cache
def get_followup_policy() -> dict:
    return _load_yaml("followup_policy.yaml")