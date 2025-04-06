# kano_db_models.py
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base  # ← これが必要！


class DailyMuscleSummary(Base):
    __tablename__ = "daily_muscle_summaries"

    id = Column(Integer, primary_key=True, index=True)
    day_label = Column(String, nullable=False)  # 例: '1日'
    major_muscle_name = Column(String, nullable=False)  # 例: '大胸筋'
    total_score = Column(Float, nullable=False)
    created_at = Column(Date, default=date.today)