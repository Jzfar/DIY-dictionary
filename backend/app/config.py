"""
配置管理 - 支持本地开发和生产环境
使用 Pydantic Settings 现代方式自动加载 .env 文件
"""
from enum import Enum
from typing import Optional
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentEnum(str, Enum):
    """环境枚举"""
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


class Settings(BaseSettings):
    """应用配置 - 自动从 .env 文件和环境变量加载"""

    # 应用
    app_name: str = Field(default="DIY Dictionary")
    app_version: str = Field(default="0.1.0")

    # 环境
    environment: EnvironmentEnum = Field(default=EnvironmentEnum.DEV)

    # API
    api_v1_str: str = Field(default="/api/v1")

    # 数据库
    database_url: Optional[str] = Field(default=None)

    # LLM API
    llm_api_key: Optional[str] = Field(default=None)
    llm_model: str = Field(default="gpt-4")
    llm_provider: str = Field(default="openai")

    # CORS
    cors_origins: list = Field(default=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ])

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def debug(self) -> bool:
        """DEBUG 模式依赖 ENVIRONMENT"""
        return self.environment == EnvironmentEnum.DEV

    @field_validator("database_url", mode="after")
    @classmethod
    def set_database_url(cls, v: Optional[str], info) -> str:
        """根据环境设置数据库 URL"""
        environment = info.data.get("environment", EnvironmentEnum.DEV)

        if environment == EnvironmentEnum.DEV:
            # 本地开发使用 SQLite
            return v or "sqlite:///./diy_dictionary.db"
        else:
            # 生产使用 PostgreSQL
            if not v:
                raise ValueError("DATABASE_URL 必须在生产环境中设置")
            return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """解析 CORS 源列表"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


@lru_cache()
def get_settings() -> Settings:
    """获取设置单例（缓存）"""
    return Settings()
