import React, { useState } from 'react'
import API from '../services/api'

const Roadmap = () => {
  const [goal, setGoal] = useState('')
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(false)

  const generate = async () => {
    setLoading(true)
    try {
      const res = await API.post('/roadmap/generate', { goal })
      setRoadmap(res.data.roadmap)
    } catch (e) {
      alert('Failed to generate roadmap')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow p-8">
        <h1 className="text-3xl font-bold mb-6">Career Roadmap</h1>
        <input
          type="text"
          placeholder="Enter your career goal (e.g. Become a Data Scientist)"
          className="border w-full p-3 rounded-xl mb-4"
          value={goal}
          onChange={e => setGoal(e.target.value)}
        />
        <button
          className="bg-indigo-600 text-white w-full py-3 rounded-xl mb-6"
          onClick={generate}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Roadmap'}
        </button>
        {roadmap && (
          <div className="bg-gray-50 p-4 rounded-xl text-gray-700 whitespace-pre-wrap">
            {roadmap}
          </div>
        )}
      </div>
    </div>
  )
}

export default Roadmap
