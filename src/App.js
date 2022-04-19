/* eslint-disable react/style-prop-object */
/* eslint-disable react-hooks/exhaustive-deps */
import React from 'react';

// import { Route, Switch } from "react-router";
import {
  BrowserRouter as Router, Route, Routes
} from 'react-router-dom';

import Create from './Create';
import Select from './Select';


import './App.css';



function App() {

  return (
    <Router>
      <Routes>
        <Route path="/selection" element={<Select />} />
        <Route path="/create_a_league" element={<Create />} />
      </Routes>
    </Router>
  )


}
export default App;
