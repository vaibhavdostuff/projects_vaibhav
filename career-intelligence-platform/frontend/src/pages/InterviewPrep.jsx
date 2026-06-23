import React, { useState } from 'react'
import API from '../services/api'

const InterviewPrep = () => {
  const [role, setRole] = useState('')
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(false)

  const generate = async () => {
    setLoading(true)
    try {
      const res = await API.post('/interview/generate', { role })
      setQuestions(res.data.questions || [])
    } catch (e) {
      alert('Failed to generate questions')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow p-8">
        <h1 className="text-3xl font-bold mb-6">Interview Prep</h1>
        <input
          type="text"
          placeholder="Enter target role (e.g. Software Engineer)"
          className="border w-full p-3 rounded-xl mb-4"
          value={role}
          onChange={e => setRole(e.target.value)}
        />
        <button
          className="bg-indigo-600 text-white w-full py-3 rounded-xl mb-6"
          onClick={generate}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Questions'}
        </button>
        {questions.length > 0 && (
          <ul className="space-y-3">
            {questions.map((q, i) => (
              <li key={i} className="bg-gray-50 p-4 rounded-xl text-gray-700">
                {i + 1}. {q}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default InterviewPrep
