"use client";

import { useState } from "react";

import { signupUser } from "@/services/authService";

export default function RegisterPage() {
  const [username, setUsername] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const handleRegister =
    async () => {
      try {
        await signupUser(
          username,
          email,
          password
        );

        alert(
          "Registration successful!"
        );

      } catch {
        alert(
          "Registration failed."
        );
      }
    };

  return (
    <div className="p-10">
      <h1 className="text-2xl mb-4">
        Register
      </h1>

      <input
        className="border p-2 block mb-4"
        placeholder="Username"
        value={username}
        onChange={(e) =>
          setUsername(e.target.value)
        }
      />

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
        onClick={handleRegister}
      >
        Register
      </button>
    </div>
  );
}
