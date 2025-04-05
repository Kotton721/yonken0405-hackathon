from database import SessionLocal
from kano_db_models import DailyMuscleSummary

def delete_all_daily_data():
    db = SessionLocal()
    try:
        deleted = db.query(DailyMuscleSummary).delete()
        db.commit()
        print(f"{deleted} 件のレコードを削除しました")
    finally:
        db.close()

if __name__ == "__main__":
    delete_all_daily_data()
