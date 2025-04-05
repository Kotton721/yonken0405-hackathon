from sqlalchemy import Column, Integer, String, ForeignKey,Float
from sqlalchemy.orm import relationship
#ローカルでpythonとして実行するときはapp.が必要がないが，uvicornで実行するときベースのdirectoryがapp/appの上の階層
from database import Base

# 大筋群
class MajorMuscle(Base):
    __tablename__ = "major_muscles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    minor_muscles = relationship("MinorMuscle", back_populates="major_muscle")
    training_names = relationship("TrainingName", back_populates="major_muscle")


# 細かい筋肉
class MinorMuscle(Base):
    __tablename__ = "minor_muscles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    major_muscle_id = Column(Integer, ForeignKey("major_muscles.id"), nullable=False, index=True)

    # リレーション
    major_muscle = relationship("MajorMuscle", back_populates="minor_muscles")
    scores = relationship("TrainingScore", back_populates="minor_muscle")


# トレーニングのタイプ
class TrainingType(Base):
    __tablename__ = "training_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    training_names = relationship("TrainingName", back_populates="training_type")


# トレーニング
class TrainingName(Base):
    __tablename__ = "training_names"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)  # トレーニング名（一意）
    major_muscle_id = Column(Integer, ForeignKey("major_muscles.id"), nullable=False, index=True)
    major_muscle = relationship("MajorMuscle", back_populates="training_names")
    # TrainingTypeとのリレーション
    training_type_id = Column(Integer, ForeignKey("training_types.id"), nullable=False, index=True)
    training_type = relationship("TrainingType", back_populates="training_names")

    scores = relationship("TrainingScore", back_populates="training_name")

    weight_ratios = relationship("WeightRatio", back_populates="training_name")


# トレーニングとスコアを保持するテーブル
class TrainingScore(Base):
    __tablename__ = "training_scores"

    id = Column(Integer, primary_key=True, index=True)
    training_name_id = Column(Integer, ForeignKey("training_names.id"), nullable=False, index=True)  # トレーニングID
    minor_muscle_id = Column(Integer, ForeignKey("minor_muscles.id"), nullable=False, index=True)
    muscle_score = Column(Integer, nullable=False)  # スコア

    # リレーション
    training_name = relationship("TrainingName", back_populates="scores")
    minor_muscle = relationship("MinorMuscle", back_populates="scores")

class WeightRatio(Base):
    __tablename__ = "weight_ratios"

    id = Column(Integer, primary_key=True, index=True)
    training_name_id = Column(Integer, ForeignKey("training_names.id"), nullable=False, index=True)
    weight_recommend = Column(Float, nullable=False)  # 推奨重量比（例: 1.5）

    training_name = relationship("TrainingName", back_populates="weight_ratios")



