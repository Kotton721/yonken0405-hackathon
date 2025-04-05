# kano.py
from sqlalchemy.orm import Session
from db_models import TrainingName, TrainingScore

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

# スコアを計算する関数
def calculate_total_training_score(
    db: Session,
    training_inputs: list[dict]  # 各要素に {training_name, reps, sets} が入る
):
    total_result = {}

    for item in training_inputs:
        name = item["training_name"]
        reps = item.get("reps", 10)
        sets = item.get("sets", 3)

        # 種目データ取得
        training = db.query(TrainingName).filter_by(name=name).first()
        if not training:
            print(f"種目「{name}」が見つかりません")
            continue

        # スコア取得
        scores = db.query(TrainingScore).filter_by(training_name_id=training.id).all()
        for score in scores:
            muscle = db.query(MinorMuscle).filter_by(id=score.minor_muscle_id).first()
            if not muscle:
                continue
            base_score = score.muscle_score
            adjusted_score = base_score * (sets / 3.0)  # 重量比率は無視

            # 合計スコアに加算
            if muscle.name in total_result:
                total_result[muscle.name] += adjusted_score
            else:
                total_result[muscle.name] = adjusted_score

    return total_result



from kano_db_models import DailyMuscleSummary
from datetime import date

# スコアを保存する関数
def save_daily_summary(db: Session, daily_data: dict):
    records = []
    for day_label, muscle_scores in daily_data.items():
        for muscle_name, score in muscle_scores.items():
            summary = DailyMuscleSummary(
                day_label=day_label,
                major_muscle_name=muscle_name,
                total_score=score,
                created_at=date.today()
            )
            records.append(summary)

    db.add_all(records)
    db.commit()
    print("日別筋肉スコアを保存しました")