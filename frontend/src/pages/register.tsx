import { useState } from "react";

import toast from "react-hot-toast";

import { useRegister } from "../hooks/useRegister";

import { useNavigate } from "react-router-dom";

export default function RegisterPage() {
    const [username, setUsername] = useState("");

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const registerMutation = useRegister();

    const navigate = useNavigate();

    const handleRegister = async () => {
        try {
            await registerMutation.mutateAsync({
                username,
                email,
                password,
            });

            toast.success("Registration successful!");

            setUsername("");
            setEmail("");
            setPassword("");

            navigate("/login");
        } catch (error) {
            console.error(error);

            toast.error("Registration failed.");
        }
    };

    return (
        <div className="max-w-md mx-auto">
            <h1 className="text-3xl font-bold mb-6">Register</h1>

            <input
                className="border p-3 w-full mb-4 rounded"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input
                className="border p-3 w-full mb-4 rounded"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <input
                className="border p-3 w-full mb-4 rounded"
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button
                className="p-3 rounded w-full"
                onClick={handleRegister}
                disabled={registerMutation.isPending}
            >
                {registerMutation.isPending
                    ? "Creating account..."
                    : "Register"}
            </button>
        </div>
    );
}
