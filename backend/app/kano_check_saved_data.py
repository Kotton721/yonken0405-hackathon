# kano_check_saved_data.py
from database import SessionLocal
from kano_db_models import DailyMuscleSummary

def check_saved_data():
    db = SessionLocal()
    try:
        records = db.query(DailyMuscleSummary).all()
        print("=== 保存されたデータ ===")
        for r in records:
            print(f"{r.day_label} | {r.major_muscle_name} | {r.total_score}点 | 登録日: {r.created_at}")
    finally:
        db.close()

if __name__ == "__main__":
    check_saved_data()
