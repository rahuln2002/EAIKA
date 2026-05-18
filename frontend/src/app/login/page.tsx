"use client";

import { useState } from "react";

import { saveToken } from "@/lib/auth";
import { loginUser } from "@/services/authService";

export default function LoginPage() {
  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const handleLogin = async () => {
    try {
      const response =
        await loginUser(
          email,
          password
        );

      saveToken(
        response.access_token
      );

      alert("Login successful!");

    } catch {
      alert("Login failed.");
    }
  };

  return (
    <div className="p-10">
      <h1 className="text-2xl mb-4">
        Login
      </h1>

      <input
        className="border p-2 block mb-4"
        placeholder="Email"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
      />

      <input
        className="border p-2 block mb-4"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <button
        className="bg-black text-white p-2"
        onClick={handleLogin}
      >
        Login
      </button>
    </div>
  );
}
