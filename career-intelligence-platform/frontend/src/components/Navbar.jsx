import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {

  const logout = () => {

    localStorage.removeItem(
      "token"
    );

    window.location.href =
      "/login";
  };

  return (

    <nav className="bg-indigo-700 text-white px-8 py-4 shadow-lg">

      <div className="flex justify-between items-center">

        <h1 className="text-2xl font-bold">
          Career Intelligence Platform
        </h1>

        <div className="space-x-6">

          <Link to="/">
            Dashboard
          </Link>

          <Link to="/roadmap">
            Roadmap
          </Link>

          <Link to="/interview">
            Interview Prep
          </Link>

          <Link to="/github">
            GitHub Analysis
          </Link>

          <button
            onClick={logout}
            className="bg-white text-indigo-700 px-4 py-2 rounded-lg"
          >
            Logout
          </button>

        </div>

      </div>

    </nav>
  );
};

export default Navbar;