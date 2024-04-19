from typing import List, Tuple

from pydantic import BaseSettings


class Settings(BaseSettings):
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: str
    FIREBASE_AUTH_URI: str
    FIREBASE_TOKEN_URI: str
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str
    FIREBASE_CLIENT_X509_CERT_URL: str
    FIREBASE_WEB_API_KEY: str

    MONGO_URI: str
    MONGO_DBNAME: str = "pricing_test"

    CONTEXTUALIZER_USERNAME: str = "admin"
    CONTEXTUALIZER_PASSWORD: str
    CONTEXTUALIZER_URL: str = "https://contextualizer.motion-s.com"

    BASIC_AUTHS_STR: str = "motions:very simple"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
BASIC_AUTHS: List[Tuple] = [
    tuple(pair.split(":")) for pair in settings.BASIC_AUTHS_STR.split(",")
]
