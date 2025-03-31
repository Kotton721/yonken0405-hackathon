# Node.js の公式イメージを使用
FROM node:22-slim
RUN npm install -g npm@11.2.0
# 作業ディレクトリの設定
WORKDIR /app

# 最初に package.json と package-lock.json をコピー
COPY package.json package-lock.json ./

# 古い依存関係を削除して再インストール
RUN npm install

# アプリケーションのコードをコピー
EXPOSE 5173

CMD ["npm", "run", "dev"]

# 必要に応じて、ビルドやデバッグ用のコマンドを追加
