from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from database import engine, Base, SessionLocal
from db_models import MajorMuscle, MinorMuscle,TrainingName,TrainingScore,TrainingType,WeightRatio

from kano_db_models import DailyMuscleSummary  # 追加
# データ追加
def add_data():
    db = SessionLocal()
    try:
        #テーブルを初期化

        # 大筋群を追加
        chest = MajorMuscle(name="胸")
        back = MajorMuscle(name="背中")
        shoulder = MajorMuscle(name="肩")
        arm = MajorMuscle(name="腕")
        leg = MajorMuscle(name="脚")

        major_muscles = [chest, back, shoulder, arm, leg]
        db.add_all(major_muscles)
        db.commit()  # ここで ID を確定させる

        # 細かい筋肉を追加
        minor_muscles = [
            MinorMuscle(name="大胸筋上部", major_muscle_id=chest.id),
            MinorMuscle(name="大胸筋下部", major_muscle_id=chest.id),
            MinorMuscle(name="広背筋", major_muscle_id=back.id),
            MinorMuscle(name="僧帽筋", major_muscle_id=back.id),
            MinorMuscle(name="三角筋前部", major_muscle_id=shoulder.id),
            MinorMuscle(name="三角筋側部", major_muscle_id=shoulder.id),
            MinorMuscle(name="上腕二頭筋", major_muscle_id=arm.id),
            MinorMuscle(name="上腕三頭筋", major_muscle_id=arm.id),
            MinorMuscle(name="大腿四頭筋", major_muscle_id=leg.id),
            MinorMuscle(name="ハムストリング", major_muscle_id=leg.id),
        ]
        db.add_all(minor_muscles)
        db.commit()

        #トレーニング種目
        bodyweight = TrainingType(name="自重")
        machine = TrainingType(name="マシン")
        free_weight = TrainingType(name="フリーウェイト")

        db.add_all([bodyweight, machine, free_weight])
        db.commit()

         # トレーニング名を追加
        training_names = [
            # 胸 (Chest)
            TrainingName(name="チェストプレス", major_muscle_id=chest.id, training_type_id=machine.id),
            TrainingName(name="ペクトラルフライ", major_muscle_id=chest.id, training_type_id=machine.id),
            TrainingName(name="ベンチプレス", major_muscle_id=chest.id, training_type_id=free_weight.id),
            TrainingName(name="インクラインベンチプレス", major_muscle_id=chest.id, training_type_id=free_weight.id),
            TrainingName(name="ダンベルフライ", major_muscle_id=chest.id, training_type_id=free_weight.id),
            TrainingName(name="腕立て伏せ（プッシュアップ）", major_muscle_id=chest.id, training_type_id=bodyweight.id),
            TrainingName(name="ディップス", major_muscle_id=chest.id, training_type_id=bodyweight.id),

            # 背中 (Back)
            TrainingName(name="ラットプルダウン", major_muscle_id=back.id, training_type_id=machine.id),
            TrainingName(name="シーテッドローイング", major_muscle_id=back.id, training_type_id=machine.id),
            TrainingName(name="デッドリフト", major_muscle_id=back.id, training_type_id=free_weight.id),
            TrainingName(name="ワンハンドダンベルローイング", major_muscle_id=back.id, training_type_id=free_weight.id),
            TrainingName(name="懸垂（プルアップ）", major_muscle_id=back.id, training_type_id=bodyweight.id),
            TrainingName(name="逆手懸垂（アンダーグリップ・チンアップ）", major_muscle_id=back.id, training_type_id=bodyweight.id),

            # 肩 (Shoulders)
            TrainingName(name="ショルダープレス", major_muscle_id=shoulder.id, training_type_id=free_weight.id),
            TrainingName(name="ショルダープレスマシン", major_muscle_id=shoulder.id, training_type_id=machine.id),
            TrainingName(name="サイドレイズ", major_muscle_id=shoulder.id, training_type_id=free_weight.id),
            TrainingName(name="パイクプッシュアップ", major_muscle_id=shoulder.id, training_type_id=bodyweight.id),

            # 腕 (Arms)
            TrainingName(name="トライセプスプレスダウン", major_muscle_id=arm.id, training_type_id=machine.id),
            TrainingName(name="バイセップスカール", major_muscle_id=arm.id, training_type_id=free_weight.id),
            TrainingName(name="バーベルカール", major_muscle_id=arm.id, training_type_id=free_weight.id),
            TrainingName(name="ダンベルカール", major_muscle_id=arm.id, training_type_id=free_weight.id),
            TrainingName(name="ハンマーカール", major_muscle_id=arm.id, training_type_id=free_weight.id),
            TrainingName(name="フレンチプレス", major_muscle_id=arm.id, training_type_id=free_weight.id),
            TrainingName(name="スカルクラッシャー（ライイングトライセプスエクステンション）", major_muscle_id=arm.id, training_type_id=free_weight.id),

            # 脚 (Legs)
            TrainingName(name="レッグプレス", major_muscle_id=leg.id, training_type_id=machine.id),
            TrainingName(name="レッグエクステンション", major_muscle_id=leg.id, training_type_id=machine.id),
            TrainingName(name="レッグカール", major_muscle_id=leg.id, training_type_id=machine.id),
            TrainingName(name="カーフレイズ", major_muscle_id=leg.id, training_type_id=machine.id),
            TrainingName(name="スクワット", major_muscle_id=leg.id, training_type_id=free_weight.id),
            TrainingName(name="ブルガリアンスクワット", major_muscle_id=leg.id, training_type_id=bodyweight.id),
            TrainingName(name="スプリットスクワット", major_muscle_id=leg.id, training_type_id=bodyweight.id),
        ]

        try:
            db.add_all(training_names)
            db.commit()
            print("トレーニング名が追加されました")
        except IntegrityError as e:
            db.rollback()
            print(f"トレーニング名の追加に失敗しました: {e}")
            raise
        added_trainings = db.query(TrainingName).all()
        for t in added_trainings:
            print(f"ID: {t.id}, Name: {t.name}, MajorMuscleID: {t.major_muscle_id}, TrainingTypeID: {t.training_type_id}")

        # トレーニングスコアの追加
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
        training_scores = []
        for training_name, muscle_scores in training_scores_data.items():
            training = db.query(TrainingName).filter_by(name=training_name).first()
            if training:
                print(f"Found: {training_name} (ID: {training.id})")
                for muscle_name, score in muscle_scores.items():
                    minor_muscle = db.query(MinorMuscle).filter_by(name=muscle_name).first()
                    if minor_muscle:
                        print(f"  Found muscle: {muscle_name} (ID: {minor_muscle.id})")
                        training_score = TrainingScore(
                            training_name_id=training.id,
                            minor_muscle_id=minor_muscle.id,
                            muscle_score=score
                        )
                        training_scores.append(training_score)
                    else:
                        print(f"  Minor muscle not found: {muscle_name}")
            else:
                print(f"Training name not found: {training_name}")

        
        try:
            db.add_all(training_scores)
            db.commit()
            print("トレーニングスコアが追加されました")
        except IntegrityError as e:
            db.rollback()
            print(f"トレーニングスコアの追加に失敗しました: {e}")
            raise
        weight_ratios = [
            # 胸 (Chest)
            WeightRatio(training_name_id=1, weight_recommend=0.8),
            WeightRatio(training_name_id=2, weight_recommend=0.7),
            WeightRatio(training_name_id=3, weight_recommend=0.95),
            WeightRatio(training_name_id=4, weight_recommend=0.85),
            WeightRatio(training_name_id=5, weight_recommend=0.4),
            WeightRatio(training_name_id=6, weight_recommend=1.2),
            WeightRatio(training_name_id=7, weight_recommend=1.2),

            # 背中 (Back)
            WeightRatio(training_name_id=8, weight_recommend=0.85),
            WeightRatio(training_name_id=9, weight_recommend=0.85),
            WeightRatio(training_name_id=10, weight_recommend=1.3),
            WeightRatio(training_name_id=11, weight_recommend=0.5),
            WeightRatio(training_name_id=12, weight_recommend=1.1),
            WeightRatio(training_name_id=13, weight_recommend=1.1),

            # 肩 (Shoulders)
            WeightRatio(training_name_id=14, weight_recommend=0.8),
            WeightRatio(training_name_id=15, weight_recommend=0.8),
            WeightRatio(training_name_id=16, weight_recommend=0.2),
            WeightRatio(training_name_id=17, weight_recommend=1.25),

            # 腕 (Arms)
            WeightRatio(training_name_id=18, weight_recommend=0.7),
            WeightRatio(training_name_id=19, weight_recommend=0.4),
            WeightRatio(training_name_id=20, weight_recommend=0.55),
            WeightRatio(training_name_id=21, weight_recommend=0.3),
            WeightRatio(training_name_id=22, weight_recommend=0.3),
            WeightRatio(training_name_id=23, weight_recommend=0.5),
            WeightRatio(training_name_id=24, weight_recommend=0.5),

            # 脚 (Legs)
            WeightRatio(training_name_id=25, weight_recommend=1.4),
            WeightRatio(training_name_id=26, weight_recommend=1),
            WeightRatio(training_name_id=27, weight_recommend=0.75),
            WeightRatio(training_name_id=28, weight_recommend=1.5),
            WeightRatio(training_name_id=29, weight_recommend=1.25),
            WeightRatio(training_name_id=30, weight_recommend=1.3),
        ]
        db.add_all(weight_ratios)
        db.commit()
        print("体重比率が挿入されました")
        return major_muscles
    except Exception as e:
        db.rollback()
        print(f"エラー: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
    add_data()
