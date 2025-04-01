import { useState } from "react";
import Output from "../components/Output";
import { sendMemo } from "../utils/memoApi";

export default function Calender() {
  const [response, setResponse] = useState("");

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">カレンダーページ</h1>
      <Output onSendMemo={(memo) => sendMemo(memo, setResponse)} />
      {response && <p className="mt-2 text-green-600">{response}</p>}
    </div>
  );
}



