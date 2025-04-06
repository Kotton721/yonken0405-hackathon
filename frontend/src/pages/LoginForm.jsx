import React, { useState } from "react";
import axios from "axios";

const LoginForm = ({ setUserId, setSuccess, setError }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // ログイン処理
  const handleLogin = async (e) => {
    e.preventDefault();
    const payload = { username, password };

    try {
      const response = await axios.post("http://localhost:8000/api/login", payload);
      const { token, user } = response.data;

      // トークンをlocalStorageに保存
      localStorage.setItem("token", token);
      setUserId(user.id);
      setSuccess(`ようこそ、${user.username}さん！`);
      setError(null);
    } catch (error) {
      setError("ログインに失敗しました。ユーザー名とパスワードを確認してください。");
      setSuccess(null);
    }
  };

  return (
    <div>
      <h2>ログイン</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>ユーザー名:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="ユーザー名を入力"
            required
          />
        </div>
        <div>
          <label>パスワード:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="パスワードを入力"
            required
          />
        </div>
        <button type="submit">ログイン</button>
      </form>
    </div>
  );
};

export default LoginForm;
