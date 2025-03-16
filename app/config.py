from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):

    DB_USERNAME: Optional[str]
    DB_PASSWORD: Optional[str]
    DB_HOST: Optional[str] = "localhost"
    DB_PORT: Optional[int] = 5432
    DB_NAME: Optional[str]

    REDIS_URL: str = "redis://localhost:6379/0"

    DB_URL: Optional[str] = None

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    FRNT_END_URL: str 

    @property
    def DATABASE_URL(self) -> str:

        if self.DB_URL:
            return self.DB_URL
        
        if not all([self.DB_USERNAME, self.DB_PASSWORD, self.DB_NAME]):
            raise ValueError(
                "Missing database configuration set appropriate values in .env file."
            )
                
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

   
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )

class SingletonWrapper:
    _instances = {}

    @staticmethod
    def get_instance(cls, *args, **kwargs):
        if cls not in SingletonWrapper._instances:
            SingletonWrapper._instances[cls] = cls(*args, **kwargs)
        return SingletonWrapper._instances[cls]



Config = SingletonWrapper.get_instance(Settings)