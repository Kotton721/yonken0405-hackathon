# kano_test.py
from sqlalchemy.orm import Session
from database import SessionLocal  # すでに使ってるDB接続
from kano import calculate_total_training_score  # 上記の関数を含むファイル名に置き換えてください

def test_total():
    db = SessionLocal()
    try:
        inputs = [
            {"training_name": "チェストプレス", "reps": 10, "sets": 3},
            {"training_name": "ダンベルフライ", "reps": 10, "sets": 3},
            {"training_name": "ベンチプレス", "reps": 10, "sets": 3},
        ]
        result = calculate_total_training_score(db, inputs)
        print("=== 合計スコア ===")
        for muscle, score in result.items():
            print(f"{muscle}: {score:.2f}")
    finally:
        db.close()

if __name__ == "__main__":
    test_total()
