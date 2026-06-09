import React, { useState } from "react";
import API from "../services/api";

const Login = () => {

  const [email, setEmail] = useState("");

  const [password, setPassword] =
    useState("");

  const loginUser = async () => {

    try {

      const response = await API.post(
        "/auth/login",
        {
          email,
          password
        }
      );

      localStorage.setItem(
        "token",
        response.data.token
      );

      alert(
        "Login Successful"
      );

      window.location.href = "/";

    } catch (error) {

      console.log(error);

      alert(
        "Invalid Credentials"
      );

    }
  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-10 rounded-2xl shadow-xl w-[400px]">

        <h1 className="text-4xl font-bold text-center mb-8">
          Login
        </h1>

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
          onClick={loginUser}
        >
          Login
        </button>

      </div>

    </div>

  );
};

export default Login;