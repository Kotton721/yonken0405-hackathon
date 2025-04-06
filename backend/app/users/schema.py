from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# TrainHistoryスキーマ
class TrainHistoryBase(BaseModel):
    training_date: datetime
    training_id: int
    training_weight: int
    training_count: int


class TrainHistoryCreate(TrainHistoryBase):
    pass


class TrainHistoryRead(TrainHistoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Userスキーマ
class UserBase(BaseModel):
    username: str
    weight: Optional[float] = None
    score_chest: Optional[float] = None
    score_back: Optional[float] = None
    score_shoulder: Optional[float] = None
    score_arm: Optional[float] = None
    score_leg: Optional[float] = None
    # score_upperpecs: Optional[float] = None
    # score_lowerpecs: Optional[float] = None
    # score_lats: Optional[float] = None
    # score_traps: Optional[float] = None
    # score_anteriordelts: Optional[float] = None
    # score_lateraldelts: Optional[float] = None
    # score_biceps: Optional[float] = None
    # score_traceps: Optional[float] = None
    # score_quadriceps: Optional[float] = None
    # score_hamstrings: Optional[float] = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    train_history: List[TrainHistoryRead] = []

    class Config:
        orm_mode = True
