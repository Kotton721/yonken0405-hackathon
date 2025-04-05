import shutil
import os
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from pydantic import BaseModel
from app.database import get_db
from app.db_models import TrainingName,MajorMuscle
from app.schema import TrainingNameSchema,MajorMuscleSchema

# ロギング設定
logging.basicConfig(filename='app.log', level=logging.INFO)  # ログレベルはINFOに設定
logger = logging.getLogger(__name__)  # ロガーを作成

app = FastAPI()

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