from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, SessionLocal
from db_models import MajorMuscle, MinorMuscle,TrainingName,TrainingScore,TrainingType

# データ追加
def add_data():
    db = SessionLocal()
    try:
        #テーブルを初期化
        db.execute(text("DELETE FROM training_scores;"))  # 先にtraining_scoresを削除
        db.execute(text("DELETE FROM training_names;"))   # 次にtraining_namesを削除
        db.execute(text("DELETE FROM training_types;"))   # 次にtraining_typesを削除
        db.execute(text("DELETE FROM minor_muscles;"))    # 次にminor_musclesを削除
        db.execute(text("DELETE FROM major_muscles;"))    # 最後にmajor_musclesを削除
        db.execute(text("TRUNCATE TABLE training_scores RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE training_scores RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE training_types RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE minor_muscles RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE major_muscles RESTART IDENTITY CASCADE;"))
        db.commit()

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

        db.add_all(training_names)
        db.commit()

        print("トレーニング名が追加されました")
        return major_muscles
    except Exception as e:
        db.rollback()
        print(f"エラー: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    add_data()
