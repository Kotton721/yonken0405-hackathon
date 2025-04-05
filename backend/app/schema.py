from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime
#pydanticによってデータベースをfastapiが扱いやすい形式に変換する(db:training_names)
#BaseModelはpythonの辞書(dict型)に変換してくれるやつ
# TrainingNameのスキーマ

class TrainingNameSchema(BaseModel):
    id: int
    name: str
    major_muscle_id: int
    training_type_id: int

    class Config:
        orm_mode = True  # SQLAlchemyのORMオブジェクトをPydanticモデルに変換可能にする

# MajorMuscleのスキーマ
class MajorMuscleSchema(BaseModel):
    id: int
    name: str
    training_names: List[TrainingNameSchema]  # ネストされたリレーション

    class Config:
        orm_mode = True

class TrainingData(BaseModel):
    training_id: int
    weight: float
    reps: int
    timestamp: datetime