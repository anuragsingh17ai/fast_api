from pydantic_settings import BaseSettings, SettingsConfigDict 
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class BaseConfig(BaseSettings):
    ENV_STATE:Optional[str] = None 

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix = "DEV_")

class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix = "PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///./test.d"
    DB_FORCE_ROLL_BACK: bool = True 

    model_config = SettingsConfigDict(env_prefix = "TEST_")

@lru_cache()
def get_config(env_stat:str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_stat]()



config = get_config(BaseConfig().ENV_STATE)