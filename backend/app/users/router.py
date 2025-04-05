from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.users.models import User, Train_History
from app.users.schema import (
    UserCreate, UserRead,
    TrainHistoryCreate, TrainHistoryRead
)

router = APIRouter()

# ユーザー作成
@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザー取得(ID指定)
@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 全ユーザー取得
@router.get("/users", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# ユーザー削除
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

# トレーニング履歴追加
@router.post("/users/{user_id}/train-history", response_model=TrainHistoryRead)
def add_train_history(
    user_id: int,
    history: TrainHistoryCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_history = Train_History(user_id=user_id, **history.dict())
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history

# トレーニング履歴取得
@router.get("/users/{user_id}/train-history", response_model=List[TrainHistoryRead])
def get_train_history(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    histories = db.query(Train_History).filter(Train_History.user_id == user_id).all()
    return histories
