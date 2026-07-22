from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    telegram_bot_token: SecretStr
    max_bot_token: SecretStr
    postgres_user: SecretStr
    postgres_password: SecretStr
    postgres_db: SecretStr
    postgres_port: SecretStr
    postgres_host: SecretStr
    ai_api_key: SecretStr
    ai_folder_id: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()
