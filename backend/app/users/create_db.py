from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # models.py から Baseをインポートします
import os
# データベースのURL(compose.ymlに書いてあるデータベース名にアクセス)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/yonken0405-db")

# データベースと接続
engine = create_engine(DATABASE_URL, echo=True)

# テーブルを作成
Base.metadata.create_all(engine)

# セッション作成（オプション）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    print("テーブルを作成しました")


