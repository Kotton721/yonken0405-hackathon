import React from 'react';
import TrainingItem from './TrainingItem';

const MuscleItem = ({ muscle, openStates, toggleMuscle, trainingOpenStates, toggleTraining, trainingRecords, currentInput, handleInputChange, saveTrainingData }) => (
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
            <TrainingItem
              key={training.id}
              training={training}
              trainingOpenStates={trainingOpenStates}
              toggleTraining={toggleTraining}
              trainingRecords={trainingRecords}
              currentInput={currentInput}
              handleInputChange={handleInputChange}
              saveTrainingData={saveTrainingData}
            />
          ))}
        </ul>
      ) : (
        <p>トレーニングが登録されていません</p>
      )
    )}
  </div>
);

export default MuscleItem;