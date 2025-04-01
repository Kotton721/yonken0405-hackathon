import axios from 'axios';
//sendMemoというfastapiと通信するsendMemoという関数を定義
export const sendMemo = async (memo, setResponse) => {
  console.log("Sending memo:", memo);  // デバッグ用のログ
  try {
    // メモをサーバーに送信
    const response = await axios.post('http://localhost:8000/memo_input', {
      memo: memo, // メモの内容
    });

    // 成功時の処理
    if (response.status === 200) {
      setResponse(`メモが送信されました: ${response.data.message}`);
    } else {
      setResponse("メモの送信に失敗しました。再試行してください。");
    }
  } catch (error) {
    // エラー発生時の処理
    setResponse(`送信中にエラーが発生しました: ${error.message}`);
    console.error("Error:", error);
  }
};
