from database import SessionLocal
from kano_db_models import DailyMuscleSummary
from collections import defaultdict

# 重み付きで集計
def calculate_weighted_muscle_scores():
    db = SessionLocal()
    try:
        # 最新の7日間のデータを day_label の降順で取得（例：'7日', ..., '1日'）
        records = db.query(DailyMuscleSummary).order_by(DailyMuscleSummary.day_label.desc()).all()

        # 日付ごとにグループ化
        day_groups = defaultdict(list)
        for r in records:
            day_groups[r.day_label].append(r)

        # day_labelの昇順で並び替え（1日目〜7日目）
        sorted_days = sorted(day_groups.keys())[-7:]

        # 重み（7日目:0.9, 6日目:0.8, ..., 1日目:0.3）
        weights = [0.3 + 0.1 * i for i in range(len(sorted_days))]

        muscle_scores = defaultdict(float)

        for day_idx, day_label in enumerate(sorted_days):
            weight = weights[day_idx]
            for r in day_groups[day_label]:
                muscle_scores[r.major_muscle_name] += r.total_score * weight

        print("=== 重み付き合計スコア ===")
        total = 0.0
        for muscle, score in muscle_scores.items():
            print(f"{muscle}: {score:.2f}")
            total += score
        print(f"\n【合計スコア】: {total:.2f}")
    finally:
        db.close()

if __name__ == "__main__":
    calculate_weighted_muscle_scores()


def get_weighted_muscle_scores():
    db = SessionLocal()
    try:
        records = db.query(DailyMuscleSummary).order_by(DailyMuscleSummary.day_label.desc()).all()
        day_groups = defaultdict(list)
        for r in records:
            day_groups[r.day_label].append(r)

        sorted_days = sorted(day_groups.keys())[-7:]
        weights = [0.3 + 0.1 * i for i in range(len(sorted_days))]

        muscle_scores = defaultdict(float)

        for day_idx, day_label in enumerate(sorted_days):
            weight = weights[day_idx]
            for r in day_groups[day_label]:
                muscle_scores[r.major_muscle_name] += r.total_score * weight

        return muscle_scores  # ← print ではなく返す
    finally:
        db.close()


