import psycopg2

# データベース接続情報
host = "db"  # もしコンテナで動いている場合はコンテナ名（例: db）
dbname = "yonken0405-db"  # データベース名を"training"に設定
user = "user"
password = "password"

# データベースに接続
conn = psycopg2.connect(
    host=host,
    dbname=dbname,
    user=user,
    password=password
)

training_name_id = 1  # 例えば1を指定

# SQLクエリ
query = """
SELECT minor_muscle_id, muscle_score
FROM training_scores
WHERE training_name_id = %s;
"""

# カーソルを作成してクエリを実行
cursor = conn.cursor()

# SQLクエリを実行して結果を取得
cursor.execute(query, (training_name_id,))

# 結果を取得
rows = cursor.fetchall()

# minor_muscle_nameを取得するクエリ
minor_muscle_query = "SELECT name FROM minor_muscles WHERE id = %s;"

# 結果を表示
for row in rows:
    minor_muscle_id = row[0]
    muscle_score = row[1]

    # minor_muscle_nameを取得
    cursor.execute(minor_muscle_query, (minor_muscle_id,))
    minor_muscle_name = cursor.fetchone()[0]

    # 出力
    print(f"minor_muscle_name: {minor_muscle_name}, muscle_score: {muscle_score}")

# 接続を閉じる
cursor.close()
conn.close()
