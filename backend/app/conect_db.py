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

# SQLクエリ: weight_ratios と training_names を結合して取得
query = """
SELECT wr.training_name_id, wr.weight_recommend, tn.name
FROM weight_ratios wr
JOIN training_names tn ON wr.training_name_id = tn.id;
"""

# カーソルを作成
cursor = conn.cursor()

# クエリを実行して結果を取得
cursor.execute(query)

# 結果を取得
rows = cursor.fetchall()

# 結果を表示
print("トレーニングごとの推奨重量比:")
for row in rows:
    training_name_id = row[0]
    weight_recommend = row[1]
    training_name = row[2]
    print(f"Training Name: {training_name}, Weight Recommend: {weight_recommend} (training_name_id: {training_name_id})")

# 接続を閉じる
cursor.close()
conn.close()