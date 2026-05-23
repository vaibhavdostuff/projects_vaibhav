import axios from 'axios'
import React, { useState } from 'react'

const ResumeUpload = () => {

  const [file, setFile] = useState(null)

  const uploadResume = async () => {

    const formData = new FormData()
    formData.append('file', file)

    const response = await axios.post(
      'http://127.0.0.1:5000/upload_resume',
      formData
    )

    console.log(response.data)
  }

  return (
    <div>
      <input
        type='file'
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadResume}>
        Upload Resume
      </button>
    </div>
  )
}

export default ResumeUpload