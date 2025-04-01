import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'
import Calender from './pages/Calender';

function App() {
  return (
    <Router>  {}
      <Routes>
        <Route path="/" element={<Calender />} />  {}
      </Routes>
  </Router>
  );
}

export default App;
