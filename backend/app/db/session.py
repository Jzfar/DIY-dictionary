"""
数据库会话管理
"""
from typing import Generator
from sqlalchemy.orm import Session

from app.db.base import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    数据库会话依赖注入

    使用方式:
        def my_endpoint(db: Session = Depends(get_db)):
            # 使用 db 进行查询
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
