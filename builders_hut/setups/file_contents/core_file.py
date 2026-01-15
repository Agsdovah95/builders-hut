from textwrap import dedent

CORE_FILE_CONTENT = dedent("""
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import Field
from functools import lru_cache

load_dotenv()


class Settings(BaseSettings):
    '''
    Settings for the application
    '''
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    TITLE: str = Field(
        description="The title of the application", validation_alias="TITLE"
    )
    DESCRIPTION: str = Field(
        description="The description of the application",
        validation_alias="DESCRIPTION",
    )
    VERSION: str = Field(
        description="The version of the application", validation_alias="VERSION"
    )
    DEBUG: bool = Field(
        description="Whether the application is in debug mode",
        validation_alias="DEBUG",
    )
    PORT: int = Field(
        description="The port to run the application on", validation_alias="PORT"
    )
    HOST: str = Field(
        description="The host to run the application on", validation_alias="HOST"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    '''
    Get the settings
    '''
    return Settings()


settings = get_settings()

""")
