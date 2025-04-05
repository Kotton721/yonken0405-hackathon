from typing import List, TypeVar
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, query

from app.users.models import Base
from app.database import get_db, SessionLocal

ModelType = TypeVar("ModelType", bound=Base)

class BaseCRUD:
    """ データアクセスクラスのベース
    """
    model: ModelType = None

    def __init__(self, db_session: SessionLocal) -> None:
        self.db_session = db_session
        self.model.query = self.db_session.query_property()

    def get_query(self) -> query.Query:
        return self.model.query

    def gets(self) -> List[ModelType]:
        """ 全件取得
        """
        return self.get_query().all()

    def get_by_id(self, id: int) -> ModelType:
        """ 主キーで取得
        """
        return self.get_query().filter_by(id=id).first()

    def create(self, data: dict = {}) -> ModelType:
        """ 新規登録
        """
        obj = self.model()
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db_session.add(obj)
        self.db_session.flush()
        self.db_session.refresh(obj)
        return obj

    def update(self, obj: ModelType, data: dict = {}) -> ModelType:
        """ 更新
        """
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db_session.flush()
        self.db_session.refresh(obj)
        return obj

    def delete_by_id(self, id: int) -> None:
        """ 主キーで削除
        """
        obj = self.get_by_id(id)
        if obj:
            self.db_session_delete(obj)
            self.db_session.flush()
        return None

