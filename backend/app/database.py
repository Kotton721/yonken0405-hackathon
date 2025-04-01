from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# データベースのURL(compose.ymlに書いてあるデータベース名にアクセス)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/yonken0405-db")

# エンジンの作成(データベースと接続)
engine = create_engine(DATABASE_URL, echo=True)

# セッションローカル(データの挿入，更新，削除を行う) engineっていうデータベースエンジンを指定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()

# データベースセッションを取得するための関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
