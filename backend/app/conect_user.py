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

# SQLクエリ: ユーザー情報とそのトレーニング履歴を取得
query = """
SELECT
    u.id AS user_id,
    u.username,
    u.weight,
    th.training_date,
    th.training_id,
    th.training_weight,
    th.training_count
FROM
    users u
JOIN
    train_history th ON u.id = th.user_id;
"""

# カーソルを作成
cursor = conn.cursor()

# クエリを実行して結果を取得
cursor.execute(query)

# 結果を取得
rows = cursor.fetchall()

# 結果を表示
print("ユーザーとトレーニング履歴:")
for row in rows:
    user_id = row[0]
    username = row[1]
    weight = row[2]
    training_date = row[3]
    training_id = row[4]  # training_id を取得
    training_weight = row[5]
    training_count = row[6]
    print(f"User ID: {user_id}, Username: {username}, Weight: {weight}, Training Date: {training_date}, "
          f"Training ID: {training_id}, Weight: {training_weight}, Reps: {training_count}")

# 接続を閉じる
cursor.close()
conn.close()
