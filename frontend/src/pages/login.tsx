import { useState } from "react";

import toast from "react-hot-toast";

import { saveToken } from "../lib/auth";
import { useLogin } from "../hooks/useLogin";

export default function LoginPage() {
    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const loginMutation = useLogin();

    const handleLogin = async () => {
        try {
            const response = await loginMutation.mutateAsync({
                email,
                password,
            });

            saveToken(response.access_token);

            toast.success("Login successful!");
        } catch {
            toast.error("Login failed.");
        }
    };

    return (
        <div className="max-w-md mx-auto p-10">
            <h1 className="text-3xl font-bold mb-6">Login</h1>

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
                className="bg-black text-white p-3 rounded w-full"
                onClick={handleLogin}
                disabled={loginMutation.isPending}
            >
                {loginMutation.isPending ? "Logging in..." : "Login"}
            </button>
        </div>
    );
}
