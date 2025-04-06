# https://qiita.com/Butterthon/items/a55daa0e7f168fee7ef0
from sqlalchemy import BOOLEAN, Column, Integer, TEXT, TIMESTAMP, VARCHAR, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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

    

class User(BaseModel):
    __tablename__ = 'users'

    username = Column(TEXT, unique=True, nullable=False)

    weight = Column(Float, nullable=True, comment='体重（kg）')

    # 部位別スコア
    # score_chest = Column(Float, nullable=True, comment='胸スコア')
    # score_back = Column(Float, nullable=True, comment='背中スコア')
    # score_shoulder = Column(Float, nullable=True, comment='肩スコア')
    # score_arm = Column(Float, nullable=True, comment='腕スコア')
    # score_leg = Column(Float, nullable=True, comment='足スコア')
    score_upperpecs = Column(Float, nullable=True, comment='大胸筋上部スコア')
    score_lowerpecs = Column(Float, nullable=True, comment='大胸筋下部スコア')
    score_lats = Column(Float, nullable=True, comment='広背筋スコア')
    score_traps = Column(Float, nullable=True, comment='僧帽筋スコア')
    score_anteriordelts = Column(Float, nullable=True, comment='三角筋前部スコア')
    score_lateraldelts = Column(Float, nullable=True, comment='三角筋側部スコア')
    score_biceps = Column(Float, nullable=True, comment='上腕二頭筋スコア')
    score_traceps = Column(Float, nullable=True, comment='上腕三頭筋スコア')
    score_quadriceps = Column(Float, nullable=True, comment='大腿四頭筋スコア')
    score_hamstrings = Column(Float, nullable=True, comment='ハムストリングススコア')

    # トレーニング履歴とのリレーション
    train_history = relationship("Train_History", back_populates="user", cascade="all, delete-orphan")


class Train_History(BaseModel):
    __tablename__ = 'train_history'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='ユーザーID')
    training_date = Column(DateTime(timezone=True), nullable=False, comment='トレーニング日')
    training_id = Column(Integer, nullable=False, comment='トレーニングID')
    training_weight = Column(Integer, nullable=False, comment='重量')
    training_count = Column(Integer, nullable=False, comment='回数')

    # Userとのリレーション
    user = relationship("User", back_populates="train_history")