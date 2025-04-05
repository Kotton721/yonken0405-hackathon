import logging
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
logging.basicConfig(filename='app.log', level=logging.INFO)  # ログレベルはINFOに設定
logger = logging.getLogger(__name__)  # ロガーを作成

# ユーザー作成
from sqlalchemy.exc import IntegrityError

@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"ユーザー作成リクエストを受信: username='{user.username}'")

    # ユーザー名が既に存在するか確認
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.warning(f"ユーザー作成失敗: username='{user.username}' は既に存在します")
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        # ユーザーを作成
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()  # コミットを実行してデータベースに保存
        db.refresh(db_user)  # 新しく作成したユーザーをリフレッシュ

        logger.info(f"ユーザー作成成功: id={db_user.id}, username='{db_user.username}'")
        return db_user

    except IntegrityError as e:
        # ユーザー名などの制約違反が発生した場合
        db.rollback()  # トランザクションをロールバック
        logger.error(f"データベースの制約違反: {e.orig}")

        if "unique constraint" in str(e.orig):
            raise HTTPException(status_code=400, detail="ユーザー名が既に使用されています。別の名前を選んでください。")
        else:
            raise HTTPException(status_code=400, detail="データベースエラーが発生しました。")

    except Exception as e:
        # その他の予期しないエラーに対する処理
        db.rollback()  # ロールバック
        logger.error(f"ユーザー作成中に予期しないエラーが発生: {e}")
        raise HTTPException(status_code=500, detail="ユーザー作成中に予期しないエラーが発生しました。")

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
