"""
测试配置 - pytest fixtures 和配置
"""
import os
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# 使用内存数据库用于测试
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """创建测试数据库"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    # 导入所有模型以创建表
    from app.db.base import Base
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    db = TestingSessionLocal()

    yield db

    db.close()
    engine.dispose()


@pytest.fixture
def client(test_db: Session):
    """创建测试客户端"""
    from app.main import app
    from app.db.session import get_db

    def override_get_db():
        return test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# pytest 配置选项
def pytest_configure(config):
    """全局 pytest 配置"""
    config.addinivalue_line(
        "markers", "integration: 集成测试"
    )
    config.addinivalue_line(
        "markers", "unit: 单元测试"
    )
