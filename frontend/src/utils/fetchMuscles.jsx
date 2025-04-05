import axios from 'axios';

export const fetchMuscles = async (setMuscles, setLoading, setError) => {
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