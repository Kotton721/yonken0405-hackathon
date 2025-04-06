import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {toggleState} from '../utils/toggleState'

function MuscleList({ date,userId,onSave, onClose }) {
  const [muscles, setMuscles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openStates, setOpenStates] = useState({}); // 筋肉のトグル状態
  const [trainingOpenStates, setTrainingOpenStates] = useState({}); // トレーニングのトグル状態
  const [trainingRecords, setTrainingRecords] = useState({}); // 保存された記録
  const [currentInput, setCurrentInput] = useState({}); // 現在の入力値

  const formattedDate = `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
  const queryDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;

  // 日付フォーマット用関数
  const formatDateString = (dateObj) => {
    return `${dateObj.getFullYear()}-${String(dateObj.getMonth() + 1).padStart(2, '0')}-${String(dateObj.getDate()).padStart(2, '0')}`;
  };

  useEffect(() => {
    const fetchMuscles = async () => {
      try {
        const response = await axios.get('http://localhost:8000/major-muscles');
        setMuscles(response.data);
      } catch (error) {
        console.error('データの取得に失敗しました:', error);
        setError('データの取得に失敗しました。');
      } finally {
        setLoading(false);
      }
    };
    fetchMuscles();
  }, []);

  useEffect(() => {
    const fetchTrainHistory = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/api/users/${userId}/train-history`);
        const data = res.data;  // axios では `.data` に格納されている

        const targetDate = formatDateString(date); // 表示したい日付（例：2025-04-06）

        // 日付で絞り込む（created_at または training_date が 'YYYY-MM-DD' 形式で返ってくる前提）
        const filtered = data.filter(record => {
          const recordDate = record.training_date || record.created_at;
          return recordDate?.slice(0, 10) === targetDate;
        });

        // トレーニングIDごとにまとめる
        const grouped = {};
        filtered.forEach((record) => {
          if (!grouped[record.training_id]) grouped[record.training_id] = [];
          grouped[record.training_id].push(record);
        });

        setTrainingRecords(grouped);
      } catch (error) {
        console.error("履歴の取得に失敗しました", error);
        setError("履歴の取得に失敗しました");
      } finally {
        setLoading(false);
      }
    };

    fetchTrainHistory();
  }, [userId, date]);




   // 筋肉のトグル
  const toggleMuscle = (muscleId) => {
    setOpenStates((prev) => toggleState(prev, muscleId));
  };

  // トレーニングのトグル
  const toggleTraining = (trainingId) => {
    setTrainingOpenStates((prev) => toggleState(prev, trainingId));
  };

  // 入力値の変更
  const handleInputChange = (trainingId, field, value) => {
    setCurrentInput((prev) => ({
      ...prev,
      [trainingId]: {
        ...prev[trainingId],
        [field]: value,
      },
    }));
  };

  // 保存ボタンが押されたとき
const saveTrainingData = async (trainingId) => {
  const data = currentInput[trainingId] || {};

  // repsとweightの両方が存在する場合のみ処理を実行
  if (data.weight && data.reps) {
    const timestamp = new Date().toISOString(); // タイムスタンプを取得

    const trainingData = {
      user_id: userId,  // ユーザーID
      training_date: queryDate,  // タイムスタンプ (トレーニング日)
      training_id: trainingId,  // トレーニングID
      training_weight: data.weight,  // 重量
      training_count: data.reps,  // 回数
    };


    try {
      // FastAPIにPOSTリクエストを送信
      const response = await axios.post(`http://localhost:8000/api/users/${userId}/train-history`, trainingData);


      // サーバーからのレスポンスを確認
      console.log("サーバーからのレスポンス:", response.data);


      // トレーニングデータを更新
      setTrainingRecords((prev) => ({
        ...prev,
        [trainingId]: [
          ...(prev[trainingId] || []),
          { weight: data.weight, reps: data.reps, timestamp }, // タイムスタンプを含めて保存
        ],
      }));

      // 入力欄をリセット
      setCurrentInput((prev) => ({
        ...prev,
        [trainingId]: { weight: '', reps: '' },
      }));
    } catch (error) {
      console.error("送信エラー:", error);
      alert("データの保存に失敗しました。");
    }
  }
};

  if (loading) {
    return <div>読み込み中...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (muscles.length === 0) {
    return <div>データがありません</div>;
  }

  return (
    <div>
      <h1>{formattedDate}</h1>
      {muscles.map((muscle) => (
        <div key={muscle.id} style={{ marginBottom: '20px' }}>
          <h2
            onClick={() => toggleMuscle(muscle.id)}
            style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}
          >
            {muscle.name}
            <span style={{ marginLeft: '10px', fontSize: '14px' }}>
              {openStates[muscle.id] ? '▲' : '▼'}
            </span>
          </h2>
          {openStates[muscle.id] && (
            muscle.training_names && muscle.training_names.length > 0 ? (
              <ul>
                {muscle.training_names.map((training) => (
                  <li key={training.id}>
                    <div
                      onClick={() => toggleTraining(training.id)}
                      style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}
                    >
                      {training.name}
                      <span style={{ marginLeft: '10px', fontSize: '12px' }}>
                        {trainingOpenStates[training.id] ? '▲' : '▼'}
                      </span>
                    </div>
                    {trainingOpenStates[training.id] && (
                      <div style={{ marginLeft: '20px', marginTop: '10px' }}>
                        {/* 保存された記録の表示 */}
                        {trainingRecords[training.id]?.length > 0 && (
                          <div style={{ marginBottom: '10px' }}>
                            <strong>記録:</strong>
                            <ul>
                              {trainingRecords[training.id].map((record, index) => (
                                <li key={index}>
                                  重さ: {record.weight || '未設定'}kg,
                                  回数: {record.reps || '未設定'},
                                  タイムスタンプ: {new Date(record.timestamp).toLocaleString('ja-JP')}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {/* 新しい入力欄 */}
                        <label>
                          重さ (kg):
                          <input
                            type="number"
                            value={currentInput[training.id]?.weight || ''}
                            onChange={(e) =>
                              handleInputChange(training.id, 'weight', e.target.value)
                            }
                            style={{ marginLeft: '5px', width: '60px' }}
                          />
                        </label>
                        <label style={{ marginLeft: '15px' }}>
                          回数:
                          <input
                            type="number"
                            value={currentInput[training.id]?.reps || ''}
                            onChange={(e) =>
                              handleInputChange(training.id, 'reps', e.target.value)
                            }
                            style={{ marginLeft: '5px', width: '60px' }}
                          />
                        </label>
                        <button
                          onClick={() => saveTrainingData(training.id)}
                          style={{ marginLeft: '15px' }}
                        >
                          保存
                        </button>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p>トレーニングが登録されていません</p>
            )
          )}
        </div>
      ))}
    </div>
  );
}

export default MuscleList;