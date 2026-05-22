import React from 'react'

const Dashboard = () => {
  return (
    <div className='p-10'>
      <h1 className='text-4xl font-bold'>
        Career Intelligence Dashboard
      </h1>

      <div className='grid grid-cols-3 gap-5 mt-10'>

        <div className='bg-white shadow-xl p-5 rounded-2xl'>
          <h2 className='text-2xl'>ATS Score</h2>
          <p className='text-5xl font-bold mt-4'>82</p>
        </div>

        <div className='bg-white shadow-xl p-5 rounded-2xl'>
          <h2 className='text-2xl'>Predicted Role</h2>
          <p className='text-3xl font-bold mt-4'>ML Engineer</p>
        </div>

        <div className='bg-white shadow-xl p-5 rounded-2xl'>
          <h2 className='text-2xl'>Skills</h2>
          <p className='mt-4'>Python, SQL, React</p>
        </div>

      </div>
    </div>
  )
}

export default Dashboard
