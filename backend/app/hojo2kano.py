from sqlalchemy.orm import Session
from app.db_models import TrainingName, TrainingScore
from app.db_models import MinorMuscle
from app.kano_db_models import DailyMuscleSummary
from app.database import SessionLocal
from collections import defaultdict
from sqlalchemy import func
from app.users.models import Train_History, User
from datetime import date, datetime, timedelta
from app.users.router import router
from app.kano_delete import delete_all_daily_data


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

        user_id = 44  # ユーザーID（必要に応じて変更）

        # スコア取得
        histories = db.query(Train_History).filter(
            Train_History.user_id == user_id,
            Train_History.training_id == training.id,
            Train_History.training_date >= datetime.now() - timedelta(days=7)  # 過去7日間
        ).all()

        # ユーザーの履歴が存在しない場合はスキップ
        if not histories:
            print(f"ユーザーID {user_id} のトレーニング履歴がありません")
            continue

        # トレーニング履歴の表示
        for history in histories:
            print(f"User ID: {history.user_id}, Training ID: {history.training_id}, "
                  f"Training Date: {history.training_date}, Weight: {history.training_weight}, "
                  f"Count: {history.training_count}")

        # スコア計算
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

# スコアを保存する関数
def save_daily_summary(db: Session, daily_data: dict):
    day_labels = list(daily_data.keys())
    db.query(DailyMuscleSummary).filter(DailyMuscleSummary.day_label.in_(day_labels)).delete(synchronize_session=False)

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

def hojo2kano(user_id: int):

    db = SessionLocal()
    try:
        daily_data = {}
        # defaultdictでリストの初期化を簡単に
        day_inputs = defaultdict(list)

        # 現在の日付を取得し、過去7日間のデータを取得する
        current_date = datetime.now()
        seven_days_ago = current_date - timedelta(days=7)

        # Train_Historyから過去7日間のデータをまとめて取得
        history_records = db.query(
            func.date(Train_History.training_date).label("training_day"),
            Train_History.training_id,
            func.count().label("sets")
        ).filter(
            Train_History.training_date >= seven_days_ago
        ).group_by(
            func.date(Train_History.training_date),
            Train_History.training_id
        ).all()

        # トレーニングID → 名前の変換（仮に辞書を使う例）
        training_name_map = {
                1: "チェストプレス",
                2: "ペクトラルフライ",
                3: "ベンチプレス",
                4: "インクラインベンチプレス",
                5: "ダンベルフライ",
                6: "腕立て伏せ（プッシュアップ）",
                7: "ディップス",
                8: "ラットプルダウン",
                9: "シーテッドローイング",
                10: "デッドリフト",
                11: "ワンハンドダンベルローイング",
                12: "懸垂（プルアップ）",
                13: "逆手懸垂（アンダーグリップ・チンアップ）",
                14: "ショルダープレス",
                15: "ショルダープレスマシン",
                16: "サイドレイズ",
                17: "パイクプッシュアップ",
                18: "トライセプスプレスダウン",
                19: "バイセップスカール",
                20: "バーベルカール",
                21: "ダンベルカール",
                22: "ハンマーカール",
                23: "フレンチプレス",
                24: "スカルクラッシャー（ライイングトライセプスエクステンション）",
                25: "レッグプレス",
                26: "レッグエクステンション",
                27: "レッグカール",
                28: "カーフレイズ",
                29: "スクワット",
                30: "ブルガリアンスクワット",
                31: "スプリットスクワット"
            }


        # 日別にinputs形式に整える
        for record in history_records:
            day_label = f"{record.training_day.day}日"  # 例：'1日'
            training_name = training_name_map.get(record.training_id, f"種目{record.training_id}")
            sets = record.sets

            day_inputs[day_label].append({
                "training_name": training_name,
                "sets": sets
            })

        # スコア計算
        for day_label, inputs in day_inputs.items():
            total_scores = calculate_total_training_score(db, inputs)
            daily_data[day_label] = total_scores

        # 保存
        save_daily_summary(db, daily_data)
    finally:
        db.close()


if __name__ == "__main__":
    delete_all_daily_data()
    hojo2kano()



# def main()
#     db = SessionLocal()
#     try:
#         daily_data = {}

#         day_inputs = {
#             "1日": [
#                 {"training_name": "チェストプレス", "sets": 2},
#                 {"training_name": "ダンベルフライ", "sets": 3},
#             ],
#             "2日": [
#                 {"training_name": "ベンチプレス", "sets": 3},
#                 {"training_name": "ショルダープレス", "sets": 2},
#             ],
#             "3日": [
#                 {"training_name": "バイセップスカール", "sets": 3},
#                 {"training_name": "スカルクラッシャー（ライイングトライセプスエクステンション）", "sets": 3},
#             ],
#             "4日": [
#                 {"training_name": "懸垂（プルアップ）", "sets": 3},
#                 {"training_name": "ラットプルダウン", "sets": 2},
#             ],
#             "5日": [
#                 {"training_name": "スクワット", "sets": 3},
#                 {"training_name": "レッグカール", "sets": 3},
#             ],
#             "6日": [
#                 {"training_name": "ブルガリアンスクワット", "sets": 2},
#                 {"training_name": "カーフレイズ", "sets": 2},
#             ],
#             "7日": [
#                 {"training_name": "パイクプッシュアップ", "sets": 2},
#                 {"training_name": "フレンチプレス", "sets": 2},
#             ]
#         }

#         for day_label, inputs in day_inputs.items():
#             total_scores = calculate_total_training_score(db, inputs)
#             daily_data[day_label] = total_scores

#         save_daily_summary(db, daily_data)
#     finally:
#         db.close()