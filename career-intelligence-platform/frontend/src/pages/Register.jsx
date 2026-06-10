import React, { useState } from "react";
import API from "../services/api";

const Register = () => {

  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const registerUser = async () => {

    try {

      await API.post(
        "/auth/register",
        {
          name,
          email,
          password
        }
      );

      alert(
        "Registration Successful"
      );

      window.location.href =
        "/login";

    } catch (error) {

      console.log(error);

      alert(
        "Registration Failed"
      );

    }
  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-10 rounded-2xl shadow-xl w-[450px]">

        <h1 className="text-4xl font-bold text-center mb-8">
          Register
        </h1>

        <input
          type="text"
          placeholder="Full Name"
          className="border w-full p-3 rounded-xl mb-4"
          value={name}
          onChange={(e) =>
            setName(
              e.target.value
            )
          }
        />

        <input
          type="email"
          placeholder="Email"
          className="border w-full p-3 rounded-xl mb-4"
          value={email}
          onChange={(e) =>
            setEmail(
              e.target.value
            )
          }
        />

        <input
          type="password"
          placeholder="Password"
          className="border w-full p-3 rounded-xl mb-4"
          value={password}
          onChange={(e) =>
            setPassword(
              e.target.value
            )
          }
        />

        <button
          className="bg-indigo-600 text-white w-full py-3 rounded-xl"
          onClick={registerUser}
        >
          Create Account
        </button>

      </div>

    </div>

  );
};

export default Register;