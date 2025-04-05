from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, timedelta

Base = declarative_base()

class TrainingRecord(Base):
    __tablename__ = 'training_record'

    training_id = Column(Integer, primary_key=True, autoincrement=True)  # 一意のID
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ユーザーID
    training_date = Column(Date, nullable=False, unique=True)  # トレーニングの日付（ユニーク）

    # 10種類のスコア（例として 'score_1', 'score_2'... としている）
    scorlumn(Float, nullable=True)
    score_4 = Column(Float, nullable=True)
    score_5 = Column(Float, nullable=True)
    score_6 = Column(Float, nullable=True)
    score_7 = Column(Float, nullable=True)
    score_8 = Column(Float, nullable=True)
    score_9 = Column(Floe_1 = Column(Float, nullable=True)
    score_2 = Column(Float, nullable=True)
    score_3 = Coat, nullable=True)
    score_10 = Column(Float, nullable=True)

    # 外部キーで関連付け
    user = relationship('User', back_populates='training_records')

    def __repr__(self):
        return f"<TrainingRecord(training_id={self.training_id}, user_id={self.user_id}, training_date={self.training_date}, " \
               f"score_1={self.score_1}, score_2={self.score_2}, ..., score_10={self.score_10})>"

    @classmethod
    def get_record_by_date(cls, session, training_date, user_id):
        """指定された日にちのトレーニング記録を取得"""
        return session.query(cls).filter(cls.training_date == training_date, cls.user_id == user_id).first()

    @classmethod
    def update_scores(cls, session, training_date, user_id, scores):
        """指定された日にちのトレーニング記録を更新する（10種類のスコアを入力）"""
        record = cls.get_record_by_date(session, training_date, user_id)
        if record:
            # スコアの更新
            record.score_1, record.score_2, record.score_3, record.score_4, record.score_5, \
            record.score_6, record.score_7, record.score_8, record.score_9, record.score_10 = scores
        else:
            # 記録がない場合、新たに作成
            new_record = cls(
                user_id=user_id,
                training_date=training_date,
                score_1=scores[0],
                score_2=scores[1],
                score_3=scores[2],
                score_4=scores[3],
                score_5=scores[4],
                score_6=scores[5],
                score_7=scores[6],
                score_8=scores[7],
                score_9=scores[8],
                score_10=scores[9]
            )
            session.add(new_record)
        session.commit()
        

def calculate_scores_for_last_7_days(session, user_id):
    """過去7日間のトレーニングスコアを算出する関数"""
    
    # 過去7日間の最初の日を計算
    seven_days_ago = date.today() - timedelta(days=7)
    
    # 過去7日間のトレーニング記録を取得
    records = session.query(TrainingRecord).filter(
        TrainingRecord.user_id == user_id,
        TrainingRecord.training_date >= seven_days_ago
    ).all()

    # スコアの合計を計算
    total_scores = [0] * 10  # score_1 ～ score_10 の合計
    num_records = len(records)  # 記録の数（7日分の記録）

    # 7日分のスコアの合計を計算
    for record in records:
        total_scores[0] += record.score_1 if record.score_1 else 0
        total_scores[1] += record.score_2 if record.score_2 else 0
        total_scores[2] += record.score_3 if record.score_3 else 0
        total_scores[3] += record.score_4 if record.score_4 else 0
        total_scores[4] += record.score_5 if record.score_5 else 0
        total_scores[5] += record.score_6 if record.score_6 else 0
        total_scores[6] += record.score_7 if record.score_7 else 0
        total_scores[7] += record.score_8 if record.score_8 else 0
        total_scores[8] += record.score_9 if record.score_9 else 0
        total_scores[9] += record.score_10 if record.score_10 else 0
    
    # 平均スコアの計算（記録があった日数で割る）
    average_scores = [score / num_records if num_records > 0 else 0 for score in total_scores]
    
    return {
        "total_scores": total_scores,   # 7日間の各スコアの合計
        "average_scores": average_scores  # 7日間の各スコアの平均
    }
    

# データベース接続
engine = create_engine('sqlite:///training.db')  # SQLiteの例
Session = sessionmaker(bind=engine)
session = Session()

# ユーザーID 1 の 2025年4月5日のトレーニング記録を更新
training_date = date(2025, 4, 5)
user_id = 1

# 10種類のスコア（例）
scores = [85.0, 90.0, 88.0, 92.5, 87.0, 89.0, 91.5, 86.5, 93.0, 90.5]

# トレーニング記録のスコアを更新
TrainingRecord.update_scores(session, training_date, user_id, scores)

# ユーザーID 1 の過去7日間のスコアを算出
scores_result = calculate_scores_for_last_7_days(session, user_id)

# 結果を表示
print("Total Scores (7 days):", scores_result["total_scores"])
print("Average Scores (7 days):", scores_result["average_scores"])