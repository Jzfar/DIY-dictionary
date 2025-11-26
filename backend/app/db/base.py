"""
SQLAlchemy 基础配置
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

settings = get_settings()

# 创建数据库引擎
# 对于 SQLite，使用 check_same_thread=False 允许在不同线程中使用
engine_kwargs = {}
if "sqlite" in settings.database_url:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # 调试模式下打印 SQL 语句
    **engine_kwargs
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 基础模型类
Base = declarative_base()
