import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MuscleList() {
    const [muscles, setMuscles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);  // エラーメッセージを管理するステート

    useEffect(() => {
      const fetchMuscles = async () => {
        try {
          const response = await axios.get('http://localhost:8000/major-muscles');
          setMuscles(response.data);  // データを状態に設定
        } catch (error) {
          console.error('データの取得に失敗しました:', error);
          setError('データの取得に失敗しました。');  // エラーメッセージの設定
        } finally {
          setLoading(false);  // ローディング状態を解除
        }
      };
      fetchMuscles();
    }, []);

    if (loading) {
      return <div>読み込み中...</div>;
    }

    if (error) {
      return <div>{error}</div>;  // エラーメッセージを表示
    }

    if (muscles.length === 0) {
      return <div>データがありません</div>;
    }

    return (
      <div>
        <h1>筋部位とトレーニング一覧</h1>
        {muscles.map((muscle) => (
          <div key={muscle.id} style={{ marginBottom: '20px' }}>
            <h2>{muscle.name}</h2>
            {muscle.training_names && muscle.training_names.length > 0 ? (
              <ul>
                {muscle.training_names.map((training) => (
                  <li key={training.id}>{training.name}</li>
                ))}
              </ul>
            ) : (
              <p>トレーニングが登録されていません</p>
            )}
          </div>
        ))}
      </div>
    );
  }

  export default MuscleList;