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

# カーソルを作成してクエリを実行
cursor = conn.cursor()

# SQLクエリを実行してテーブル内容を取得
cursor.execute("SELECT * FROM training_names;")  # trainingテーブルの内容を取得

# 結果を取得
rows = cursor.fetchall()

# 結果を表示
for row in rows:
    print(row)

# 接続を閉じる
cursor.close()
conn.close()
