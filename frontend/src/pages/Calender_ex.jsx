import React, { useState, useEffect } from "react";
import "../App.css";
import axios from "axios";
import MuscleList from "./MainPage";

// 筋トレメニューのデータ
const workoutCategories = {
  胸: ["ベンチプレス", "腕立て伏せ", "ダンベルフライ"],
  脚: ["スクワット", "レッグプレス", "ランジ"],
  背中: ["デッドリフト", "ラットプルダウン", "ベントオーバーロウ"],
  腕: ["バーベルカール", "ダンベルカール", "トライセプスプッシュダウン"],
  肩: ["ショルダープレス", "サイドレイズ", "フロントレイズ"],
};

const WorkoutCalendar = () => {
  const [workouts, setWorkouts] = useState({});
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedExercise, setSelectedExercise] = useState("");
  const [reps, setReps] = useState("");
  const [sets, setSets] = useState("");
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
  const [weight, setWeight] = useState(""); // 体重
  const [recommendedWorkout, setRecommendedWorkout] = useState(""); // おすすめメニュー
  const [username, setUsername] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [userId, setUserId] = useState(null);
  const [sentData, setSentData] = useState(null); // 送信データ
  const [responseData, setResponseData] = useState(null); // レスポンスデータ
  const [responseId, setResponseId] = useState(null); // レスポンスのID
  const [errorDetail, setErrorDetail] = useState(null); // エラー詳細


  // ローカルストレージからデータをロード
  useEffect(() => {
    const savedWorkouts = JSON.parse(localStorage.getItem("workouts"));
    if (savedWorkouts) {
      setWorkouts(savedWorkouts);
    }
  }, []);

  // データをローカルストレージに保存
  useEffect(() => {
    localStorage.setItem("workouts", JSON.stringify(workouts));
  }, [workouts]);

  // 月のカレンダーを生成
  const generateCalendar = (month, year) => {
    const startOfMonth = new Date(year, month, 1);
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDay = startOfMonth.getDay(); // 月の1日が何曜日かを取得

    let days = [];
    for (let i = 0; i < firstDay; i++) {
      days.push(null); // 空白の日を追加
    }
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(i);
    }
    return days;
  };

  // 今日のおすすめメニューを選ぶロジック（例:ランダムで選ぶ）


  const getRecommendedWorkout = async () => {
    try {
      // バックエンドからおすすめトレーニングを取得
      const response = await axios.get("http://localhost:8000/recommended-workout", {
        headers: { "Content-Type": "application/json" },
        timeout: 10000,
      });

      // バックエンドから返ってきたデータ（例：{"recommended_workouts": [...]}）
      const recommendedWorkouts = response.data.recommended_workouts;

      // レスポンスデータを使って表示する
      setRecommendedWorkout(`今日のおすすめ: ${recommendedWorkouts.join(', ')}`);

    } catch (error) {
      console.error("エラーが発生しました", error);
      setRecommendedWorkout("おすすめトレーニングの取得に失敗しました");
    }
  };


  // 曜日のリスト
  const weekdays = ["日", "月", "火", "水", "木", "金", "土"];

  // カレンダーの日付リスト
  const days = generateCalendar(currentMonth, currentYear);

  // 体重の入力が変更されたとき
  const handleWeightChange = (e) => {
    setWeight(e.target.value);
  };

  // 筋トレ記録を保存
  const handleWorkoutSubmit = (date) => {
    const key = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
    const newWorkouts = { ...workouts };
    newWorkouts[key] = { exercise: selectedExercise, reps, sets };
    setWorkouts(newWorkouts);
    setSelectedDate(null);
    setSelectedCategory("");
    setSelectedExercise("");
    setReps("");
    setSets("");
  };

  // 前月に切り替え
  const goToPreviousMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11);
      setCurrentYear(currentYear - 1);
    } else {
      setCurrentMonth(currentMonth - 1);
    }
  };

  // 翌月に切り替え
  const goToNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0);
      setCurrentYear(currentYear + 1);
    } else {
      setCurrentMonth(currentMonth + 1);
    }
  };


  // ユーザーIDの変更を処理
  const handleUseridChange = (e) => {
    setUserid(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      username: username,
      weight: weight ? parseFloat(weight) : null,
    };
    setSentData(JSON.stringify(payload));
    setResponseData(null);
    setResponseId(null);
    setErrorDetail(null);

    try {
      const response = await axios.post("http://localhost:8000/api/users", payload, {
        headers: { "Content-Type": "application/json" },
        timeout: 10000,
      });

      setResponseData(JSON.stringify(response.data));
      setResponseId(response.data.id);
      setUserId(response.data.id);

      // 新規作成またはログインの判別なく、そのまま成功メッセージ
      setSuccess(`ユーザー ${response.data.username} が処理されました！`);
      setError(null);
    } catch (error) {
      setError(error.response?.data?.detail || "エラーが発生しました");
      setErrorDetail(JSON.stringify(error.response || error.message));
      setSuccess(null);
    }
  };


  return (
    <div className="calendar-container">
      <h1>筋トレカレンダー</h1>

      {/* ユーザー作成フォーム */}
      <div>
        <h1>ユーザー作成 / ログイン</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>ユーザー名:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="ユーザー名を入力"
            />
          </div>
          <div>
            <label>体重（任意）:</label>
            <input
              type="number"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              placeholder="体重を入力"
            />
          </div>
          <button type="submit">作成 / ログイン</button>
        </form>

        {/* メッセージ表示 */}
        {success && <p style={{ color: "green" }}>{success}</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {userId && <p>現在のユーザーID: {userId}</p>}

        {/* デバッグ情報表示 */}
        {/* <div style={{ marginTop: "20px", background: "#f0f0f0", padding: "10px" }}>
          <h3>デバッグ情報</h3>
          {sentData && <p>送信データ: {sentData}</p>}
          {responseData && <p>レスポンス: {responseData}</p>}
          {responseId !== null && <p>レスポンスのID: {responseId}</p>}
          {errorDetail && <p>エラー詳細: {errorDetail}</p>}
        </div> */}
      </div>


      <div className="month-navigation">
        <button onClick={goToPreviousMonth} className="nav-button">
          前月
        </button>
        <h2>{`${currentYear}年${currentMonth + 1}月`}</h2>
        <button onClick={goToNextMonth} className="nav-button">
          翌月
        </button>
      </div>

      <div className="calendar">
        {/* 曜日表示 */}
        <div className="weekday-header">
          {weekdays.map((weekday) => (
            <div key={weekday} className="weekday">
              {weekday}
            </div>
          ))}
        </div>

        <div className="day-grid">
          {days.map((day, index) => (
            <div
              key={index}
              className={`day ${day ? "" : "empty"}`}
              onClick={() =>
                day && setSelectedDate(new Date(currentYear, currentMonth, day))
              }
            >
              {day ? day : ""}
              {/* 筋トレ記録があれば表示 */}
              {workouts[`${currentYear}-${currentMonth}-${day}`] && (
                <div className="workout-summary">
                  {workouts[`${currentYear}-${currentMonth}-${day}`].exercise}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {selectedDate && (
  <MuscleList
    date={selectedDate}
    userId={userId}  // ユーザーIDを渡す
    onSave={(date) => handleWorkoutSubmit(date)}
    onClose={() => setSelectedDate(null)}
  />
  )}

      <div className="recommended-workout">
        <button onClick={getRecommendedWorkout} className="recommend-button">
          今日のおすすめトレーニング
        </button>
        {recommendedWorkout && <p>{recommendedWorkout}</p>}
      </div>
    </div>
  );
};

export default WorkoutCalendar;