import shutil
import os
import logging
from fastapi import FastAPI, File, UploadFile,Depends,HTTPException,APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone
#データベース系
from app.database import get_db
from app.db_models import TrainingName,MajorMuscle,TrainingLog
from app.schema import TrainingNameSchema,MajorMuscleSchema,TrainingData
from app.users.router import router as user_router

from app.users.models import User
from app.users.schema import UserRead,UserCreate

from app.kano_q import QLearningTrainingSelection

minor_muscles = [
    {"name": "大胸筋上部", "major_muscle_id": "chest_id"},
    {"name": "大胸筋下部", "major_muscle_id": "chest_id"},
    {"name": "広背筋", "major_muscle_id": "back_id"},
    {"name": "僧帽筋", "major_muscle_id": "back_id"},
    {"name": "三角筋前部", "major_muscle_id": "shoulder_id"},
    {"name": "三角筋側部", "major_muscle_id": "shoulder_id"},
    {"name": "上腕二頭筋", "major_muscle_id": "arm_id"},
    {"name": "上腕三頭筋", "major_muscle_id": "arm_id"},
    {"name": "大腿四頭筋", "major_muscle_id": "leg_id"},
    {"name": "ハムストリング", "major_muscle_id": "leg_id"},
]

training_scores_data = {
    "チェストプレス": {"大胸筋上部": 35, "大胸筋下部": 30, "三角筋前部": 15, "上腕三頭筋": 20},
    "ペクトラルフライ": {"大胸筋上部": 45, "大胸筋下部": 45, "三角筋前部": 10},
    "ベンチプレス": {"大胸筋上部": 30, "大胸筋下部": 30, "三角筋前部": 15, "上腕三頭筋": 25},
    "インクラインベンチプレス": {"大胸筋上部": 50, "大胸筋下部": 20, "三角筋前部": 15, "上腕三頭筋": 15},
    "ダンベルフライ": {"大胸筋上部": 45, "大胸筋下部": 45, "三角筋前部": 10},
    "腕立て伏せ（プッシュアップ）": {"大胸筋上部": 35, "大胸筋下部": 35, "三角筋前部": 15, "上腕三頭筋": 15},
    "ディップス": {"大胸筋下部": 50, "上腕三頭筋": 40, "大胸筋上部": 10},
    "ラットプルダウン": {"広背筋": 60, "僧帽筋": 20, "上腕二頭筋": 20},
    "シーテッドローイング": {"広背筋": 50, "僧帽筋": 30, "上腕二頭筋": 20},
    "デッドリフト": {"広背筋": 30, "僧帽筋": 20, "ハムストリング": 30, "大腿四頭筋": 20},
    "ワンハンドダンベルローイング": {"広背筋": 60, "僧帽筋": 20, "上腕二頭筋": 20},
    "懸垂（プルアップ）": {"広背筋": 60, "上腕二頭筋": 30, "僧帽筋": 10},
    "逆手懸垂（アンダーグリップ・チンアップ）": {"広背筋": 50, "上腕二頭筋": 40, "僧帽筋": 10},
    "ショルダープレス": {"三角筋前部": 50, "三角筋側部": 30, "上腕三頭筋": 20},
    "ショルダープレスマシン": {"三角筋前部": 50, "三角筋側部": 30, "上腕三頭筋": 20},
    "サイドレイズ": {"三角筋側部": 80, "三角筋前部": 20},
    "パイクプッシュアップ": {"三角筋前部": 60, "上腕三頭筋": 30, "三角筋側部": 10},
    "トライセプスプレスダウン": {"上腕三頭筋": 100},
    "バイセップスカール": {"上腕二頭筋": 100},
    "バーベルカール": {"上腕二頭筋": 100},
    "ダンベルカール": {"上腕二頭筋": 100},
    "ハンマーカール": {"上腕二頭筋": 100},
    "フレンチプレス": {"上腕三頭筋": 100},
    "スカルクラッシャー（ライイングトライセプスエクステンション）": {"上腕三頭筋": 100},
    "レッグプレス": {"大腿四頭筋": 60, "ハムストリング": 40},
    "レッグエクステンション": {"大腿四頭筋": 100},
    "レッグカール": {"ハムストリング": 100},
    "スクワット": {"大腿四頭筋": 55, "ハムストリング": 45},
    "ブルガリアンスクワット": {"大腿四頭筋": 60, "ハムストリング": 40},
    "スプリットスクワット": {"大腿四頭筋": 60, "ハムストリング": 40}
}

q_learning = QLearningTrainingSelection(minor_muscles, training_scores_data)
# ロギング設定
logging.basicConfig(filename='app.log', level=logging.INFO)  # ログレベルはINFOに設定
logger = logging.getLogger(__name__)  # ロガーを作成

app = FastAPI()
router=APIRouter()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ReactフロントエンドのURLを指定
    allow_credentials=True,
    allow_methods=["*"],  # 必要に応じてHTTPメソッドを制限
    allow_headers=["*"],  # 必要に応じてヘッダーを制限
)

# MemoInput クラスの定義
class MemoInput(BaseModel):
    memo: str
training_records = []

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/memo_input")
async def receive_memo(memo_data: MemoInput):
    log_message = f"Received memo: {memo_data.memo}"
    logging.info(log_message)  # メモをログに記録
    return {"message": f"Received: {memo_data.memo}"}  # メモをレスポンスとして返す

#トレーニングの一覧を表示
@app.get("/major-muscles", response_model=List[MajorMuscleSchema])
def get_all_major_muscles(db: Session = Depends(get_db)):
    # Reactからのリクエストを受けたことをログに記録
    logger.info("Reactからの'/major-muscles'リクエストを受信")
    major_muscles = db.query(MajorMuscle).all()
    # 成功した場合、レスポンスを返す前にログを記録
    logger.info(f"取得した筋肉データ数: {len(major_muscles)}")
    return major_muscles

@app.post("/save-training")
async def save_training(data: TrainingData, db: Session = Depends(get_db)):
    logger.info("Reactからの'/save-training'リクエストを受信")
    try:
        logger.debug(f"受け取ったデータ: {data.dict()}")

         # データベースにレコードを追加
        new_log = TrainingLog(
            training_id=data.training_id,
            weight=data.weight,
            reps=data.reps,
            timestamp = datetime.fromisoformat(data.timestamp.rstrip('Z')).replace(tzinfo=timezone.utc)
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)

        return {"message": "Training data saved successfully"}
    except Exception as e:
        logger.error(f"Error saving training data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while saving data: {str(e)}")
@app.get("/recommended-workout")
def get_recommended_workout():
    logger
    current_scores = [0.0] * len(minor_muscles)  # 仮の現在のスコア
    target_scores = [150.0] * len(minor_muscles)  # 仮の目標スコア

    top_5_actions, _, _ = q_learning.q_learning_training_selection(current_scores, target_scores)

    return {"recommended_workouts": top_5_actions}
# users関連のAPIルーターを登録
app.include_router(user_router, prefix="/api")
