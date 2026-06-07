import React from "react";
import { Link } from "react-router-dom";

const Sidebar = () => {

  return (

    <div className="w-64 bg-gray-900 text-white min-h-screen p-6">

      <h2 className="text-3xl font-bold mb-10">
        Dashboard
      </h2>

      <ul className="space-y-5">

        <li>
          <Link to="/">
            Home
          </Link>
        </li>

        <li>
          <Link to="/resume">
            Resume Analysis
          </Link>
        </li>

        <li>
          <Link to="/roadmap">
            Career Roadmap
          </Link>
        </li>

        <li>
          <Link to="/interview">
            Interview Prep
          </Link>
        </li>

        <li>
          <Link to="/github">
            GitHub Analysis
          </Link>
        </li>

        <li>
          <Link to="/jobs">
            Job Recommendations
          </Link>
        </li>

      </ul>

      <div className="mt-20">

        <div className="bg-indigo-700 p-4 rounded-xl">

          <h3 className="font-bold">
            AI Career Assistant
          </h3>

          <p className="text-sm mt-2">
            Analyze resumes, predict roles,
            prepare interviews, and build
            career roadmaps.
          </p>

        </div>

      </div>

    </div>
  );
};

export default Sidebar;