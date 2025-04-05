from database import SessionLocal
from kano import calculate_total_training_score, save_daily_summary

def run_7_days():
    db = SessionLocal()
    try:
        daily_data = {}

        day_inputs = {
            "1日": [
                {"training_name": "チェストプレス", "sets": 2},
                {"training_name": "ダンベルフライ", "sets": 3},
            ],
            "2日": [
                {"training_name": "ベンチプレス", "sets": 3},
                {"training_name": "ショルダープレス", "sets": 2},
            ],
            "3日": [
                {"training_name": "バイセップスカール", "sets": 3},
                {"training_name": "スカルクラッシャー（ライイングトライセプスエクステンション）", "sets": 3},
            ],
            "4日": [
                {"training_name": "懸垂（プルアップ）", "sets": 3},
                {"training_name": "ラットプルダウン", "sets": 2},
            ],
            "5日": [
                {"training_name": "スクワット", "sets": 3},
                {"training_name": "レッグカール", "sets": 3},
            ],
            "6日": [
                {"training_name": "ブルガリアンスクワット", "sets": 2},
                {"training_name": "カーフレイズ", "sets": 2},
            ],
            "7日": [
                {"training_name": "パイクプッシュアップ", "sets": 2},
                {"training_name": "フレンチプレス", "sets": 2},
            ]
        }

        for day_label, inputs in day_inputs.items():
            total_scores = calculate_total_training_score(db, inputs)
            daily_data[day_label] = total_scores

        save_daily_summary(db, daily_data)
    finally:
        db.close()

if __name__ == "__main__":
    run_7_days()
