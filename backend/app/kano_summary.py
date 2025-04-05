from database import SessionLocal
from kano import calculate_total_training_score, save_daily_summary

if __name__ == "__main__":
    db = SessionLocal()
    try:
        # 例: 「1日」のトレーニング記録
        inputs = [
            {"training_name": "チェストプレス", "sets": 2},
            {"training_name": "ダンベルフライ", "sets": 3},
            {"training_name": "ベンチプレス", "sets": 1},
        ]

        # スコアを合計
        total_scores = calculate_total_training_score(db, inputs)

        # データを保存するための辞書形式に変換
        daily_data = {"1日": total_scores}
        save_daily_summary(db, daily_data)

    finally:
        db.close()
