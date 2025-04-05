from pydantic import BaseModel
from typing import List,Optional
#pydanticによってデータベースをfastapiが扱いやすい形式に変換する(db:training_names)
#BaseModelはpythonの辞書(dict型)に変換してくれるやつ
# TrainingNameのスキーマ
class TrainingNameSchema(BaseModel):
    id: int
    name: str
    major_muscle_id: int
    training_type_id: int

    class Config:
        orm_mode = True

class MajorMuscleSchema(BaseModel):
    id: int
    name: str
    training_names: List[TrainingNameSchema]
    class Config:
        orm_mode = True