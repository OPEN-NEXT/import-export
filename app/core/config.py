import os
import sys
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, HttpUrl, PostgresDsn, validator
from pydantic.tools import parse_obj_as


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    WIKIFACTORY_API_BASE_URL: AnyHttpUrl = parse_obj_as(
        AnyHttpUrl, "https://wikifactory.com"
    )

    @validator("WIKIFACTORY_API_BASE_URL", pre=True)
    def wikifactory_base_url(cls, v: Union[str, AnyHttpUrl]) -> AnyHttpUrl:
        if isinstance(v, str):
            return parse_obj_as(AnyHttpUrl, v)
        elif isinstance(v, AnyHttpUrl):
            return v
        raise ValueError(v)

    WIKIFACTORY_API_HOST: Optional[str] = None

    @validator("WIKIFACTORY_API_HOST")
    def wikifactory_host_from_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        api_base_url = values.get("WIKIFACTORY_API_BASE_URL")
        if api_base_url:
            if api_base_url.port:
                return f"{api_base_url.host}:{api_base_url.port}"
            return api_base_url.host

        raise ValueError(api_base_url)

    EXPORTER_GIT_MAIL: Optional[str] = None
    EXPORTER_GIT_USER: Optional[str] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if not v:
            return None
        return v

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    PYTEST_POSTGRES_SERVER: Optional[str]
    PYTEST_POSTGRES_USER: Optional[str]
    PYTEST_POSTGRES_PASSWORD: Optional[str]
    PYTEST_POSTGRES_DB: Optional[str]

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        if "pytest" in sys.modules:
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("PYTEST_POSTGRES_USER"),
                password=values.get("PYTEST_POSTGRES_PASSWORD"),
                host=values.get("PYTEST_POSTGRES_SERVER"),
                path=f"/{values.get('PYTEST_POSTGRES_DB') or ''}",
            )
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # TODO - define validations
    JOBS_BASE_PATH: str

    @validator("JOBS_BASE_PATH", pre=True)
    def ensure_download_path(cls, v: str) -> str:
        if "pytest" in sys.modules:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            return os.path.normpath(os.path.join(current_dir, "../tests/test_files"))

        # if directory can't be written, raise ValueError(v)
        return v

    BROKER_URL: Optional[AnyUrl]

    class Config:
        case_sensitive = True


settings = Settings()
