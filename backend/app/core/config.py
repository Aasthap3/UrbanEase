import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / '.env')
load_dotenv(PROJECT_ROOT / 'backend' / '.env')


class Settings:
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg://urbanease:urbanease@localhost:5432/urbanease',
    )
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'urbanease')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'urbanease')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'urbanease')
    JWT_SECRET = os.getenv('JWT_SECRET', 'change-me-in-production')


settings = Settings()
