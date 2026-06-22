import React, { useState } from 'react'
import API from '../services/api'

const GitHubAnalysis = () => {
  const [username, setUsername] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyze = async () => {
    setLoading(true)
    try {
      const res = await API.post('/github/analyze', { username })
      setResult(res.data.data)
    } catch (e) {
      alert('Failed to analyze GitHub profile')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow p-8">
        <h1 className="text-3xl font-bold mb-6">GitHub Analysis</h1>
        <input
          type="text"
          placeholder="Enter GitHub username"
          className="border w-full p-3 rounded-xl mb-4"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <button
          className="bg-indigo-600 text-white w-full py-3 rounded-xl mb-6"
          onClick={analyze}
          disabled={loading}
        >
          {loading ? 'Analysing...' : 'Analyse Profile'}
        </button>
        {result && (
          <pre className="bg-gray-50 p-4 rounded-xl text-sm text-gray-700 overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  )
}

export default GitHubAnalysis
