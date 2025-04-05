import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'
import Calender from './pages/Calender';
import MuscleList from './pages/MainPage';
import WorkoutCalendar from './pages/Calender_ex'

function App() {
  return (
    <Router>  {}
      <Routes>
        {/* <Route path="/" element={<MuscleList />} />  {} */}
        {/* <Route path="/" element={<Calender />} />  {} */}
        <Route path="/" element={<WorkoutCalendar />} />  {}
      </Routes>
  </Router>
  );
}

export default App;
