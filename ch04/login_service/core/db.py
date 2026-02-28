"""
数据库基础模块
提供数据库引擎和会话管理
"""
from sqlmodel import create_engine, Session, SQLModel

# SQLite 数据库文件路径
DATABASE_URL = "sqlite:///./user.db"

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 设置为 True 可查看 SQL 语句
    connect_args={"check_same_thread": False}  # 允许多线程访问
)


def create_tables():
    """创建所有表"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """获取数据库会话"""
    return Session(engine)
