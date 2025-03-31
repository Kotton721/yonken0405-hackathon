import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    watch: {
      usePolling: true, // ポーリングを有効化
      interval: 1000 // チェック間隔（ミリ秒）
    },
    host: '0.0.0.0', // コンテナ外からのアクセスを許可
    port: 5173, // Viteのデフォルトポート
    hmr: {
      host: 'localhost', // ローカルホストに接続
      port: 5173,
      protocol: 'ws'
    },
  }
});