from crud import BaseCRUD
from users.models import User


class CRUDUser(BaseCRUD):
    """ ユーザーデータアクセスクラスのベース
    """
    model = User

    def __init__(self, db_session: SessionLocal):
        super().__init__(db_session)
