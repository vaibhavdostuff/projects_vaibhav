import React, { useState } from "react";
import API from "../services/api";

const ResumeUpload = () => {

  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const uploadResume = async () => {

    if (!file) {
      alert("Please select a resume");
      return;
    }

    try {

      setLoading(true);

      const formData = new FormData();

      formData.append(
        "file",
        file
      );

      const response = await API.post(
        "/resume/upload",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data"
          }
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);

      alert(
        "Resume Upload Failed"
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8">

      <h2 className="text-2xl font-bold mb-6">
        Resume Analysis
      </h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <button
        className="bg-indigo-600 text-white px-6 py-3 rounded-xl mt-5"
        onClick={uploadResume}
      >
        {
          loading
            ? "Uploading..."
            : "Analyze Resume"
        }
      </button>

      {
        result && (
          <div className="mt-8">

            <div className="mb-5">

              <h3 className="font-bold text-xl">
                ATS Score
              </h3>

              <p className="text-4xl font-bold text-green-600">
                {result.ats_score}
              </p>

            </div>

            <div>

              <h3 className="font-bold text-xl">
                Skills Found
              </h3>

              <ul className="list-disc pl-5 mt-3">

                {
                  result.skills.map(
                    (skill, index) => (
                      <li key={index}>
                        {skill}
                      </li>
                    )
                  )
                }

              </ul>

            </div>

          </div>
        )
      }

    </div>
  );
};

export default ResumeUpload;