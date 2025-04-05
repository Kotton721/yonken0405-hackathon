import React from 'react';

const TrainingItem = ({ training, trainingOpenStates, toggleTraining, trainingRecords, currentInput, handleInputChange, saveTrainingData }) => (
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
                  重さ: {record.weight || '未設定'}kg, 回数: {record.reps || '未設定'}
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
            onChange={(e) => handleInputChange(training.id, 'weight', e.target.value)}
            style={{ marginLeft: '5px', width: '60px' }}
          />
        </label>
        <label style={{ marginLeft: '15px' }}>
          回数:
          <input
            type="number"
            value={currentInput[training.id]?.reps || ''}
            onChange={(e) => handleInputChange(training.id, 'reps', e.target.value)}
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
);

export default TrainingItem;