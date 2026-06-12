import React from 'react'

import {
  BrowserRouter,
  Routes,
  Route
} from 'react-router-dom'

import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Register from './pages/Register'

import InterviewPrep from './pages/InterviewPrep'
import Roadmap from './pages/Roadmap'
import GitHubAnalysis from './pages/GitHubAnalysis'

import Navbar from './components/Navbar'

function App() {

  return (

    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route
          path='/'
          element={<Dashboard />}
        />

        <Route
          path='/login'
          element={<Login />}
        />

        <Route
          path='/register'
          element={<Register />}
        />

        <Route
          path='/interview'
          element={<InterviewPrep />}
        />

        <Route
          path='/roadmap'
          element={<Roadmap />}
        />

        <Route
          path='/github'
          element={<GitHubAnalysis />}
        />

      </Routes>

    </BrowserRouter>

  )
}

export default App