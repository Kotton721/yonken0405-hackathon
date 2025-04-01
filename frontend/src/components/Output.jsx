import { useState } from "react";

export default function Output({ onSendMemo }) {
  const [message, setMessage] = useState("");

  return (
    <div className="p-4">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="メモを入力"
        className="border p-2"
      />
      <button
        onClick={() => onSendMemo(message)}
        className="ml-2 bg-blue-500 text-white p-2"
      >
        送信
      </button>
    </div>
  );
}
