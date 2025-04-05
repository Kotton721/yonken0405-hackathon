import psycopg2

# データベース接続情報
host = "db"  # コンテナ名（例: db）
dbname = "yonken0405-db"  # データベース名
user = "user"
password = "password"

# データベースに接続
conn = psycopg2.connect(
    host=host,
    dbname=dbname,
    user=user,
    password=password
)

# SQLクエリ: ユーザー情報を取得
query = """
SELECT id, username, weight, score_chest, score_back, score_shoulder, score_arm, score_leg
FROM users;
"""

# カーソルを作成
cursor = conn.cursor()

# クエリを実行して結果を取得
cursor.execute(query)

# 結果を取得
rows = cursor.fetchall()

# 結果を表示
print("ユーザー情報:")
for row in rows:
    user_id = row[0]
    username = row[1]
    weight = row[2]
    score_chest = row[3]
    score_back = row[4]
    score_shoulder = row[5]
    score_arm = row[6]
    score_leg = row[7]
    print(f"User ID: {user_id}, Username: {username}, Weight: {weight}, Chest Score: {score_chest}, Back Score: {score_back}, Shoulder Score: {score_shoulder}, Arm Score: {score_arm}, Leg Score: {score_leg}")

# 接続を閉じる
cursor.close()
conn.close()
