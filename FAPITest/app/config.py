from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname :str
    database_port :str
    database_password : str
    database_name :str
    secret_key :str
    algorithm : str
    access_token_expiration_time_minutes : int
    class Config():
        env_file=".env"

settings = Settings()