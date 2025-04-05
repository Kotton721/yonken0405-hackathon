# https://qiita.com/Butterthon/items/a55daa0e7f168fee7ef0
from sqlalchemy import BOOLEAN, Column, Integer, TEXT, TIMESTAMP, VARCHAR, Float
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql.functions import current_timestamp

# ベースクラスの作成(ORMモデル)
Base = declarative_base()

class BaseModel(Base):
    "ベースモデル"
    __abstract__ = True

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    created_at = Column(
        'created_at',
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment='登録日時',
    )

    updated_at = Column(
        'updated_at',
        TIMESTAMP(timezone=True),
        onupdate=current_timestamp(),
        comment='最終更新日時',
    )

    @declared_attr
    def __mapper_args__(cls):
        """ デフォルトのオーダリングは主キーの昇順
        
        降順にしたい場合
        from sqlalchemy import desc
        # return {'order_by': desc('id')}
        """
        return {'order_by': 'id'}
    
    
class User(BaseModel):
    __tablename__ = 'users'

    username = Column(TEXT, unique=True, nullable=False)
    password = Column(VARCHAR(128), nullable=False)

    weight = Column(Float, nullable=True, comment='体重（kg）')

    # 部位別スコア
    score_chest = Column(Float, nullable=True, comment='胸スコア')
    score_back = Column(Float, nullable=True, comment='背中スコア')
    score_shoulder = Column(Float, nullable=True, comment='肩スコア')
    score_arm = Column(Float, nullable=True, comment='腕スコア')
    score_leg = Column(Float, nullable=True, comment='足スコア')