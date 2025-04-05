from crud import BaseCRUD
from users.models import Train_History


class CRUDTrain_History(BaseCRUD):
    """ ユーザーデータアクセスクラスのベース
    """
    model = Train_History

    def __init__(self, db_session: SessionLocal):
        super().__init__(db_session)