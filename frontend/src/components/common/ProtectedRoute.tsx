import { Navigate } from "react-router-dom";

import { getToken } from "../../lib/auth";

import toast from "react-hot-toast";

export default function ProtectedRoute({
    children,
}: {
    children: React.ReactNode;
}) {
    const token = getToken();

    if (!token) {
        toast.error("Login First.");
        return <Navigate to="/login" replace />;
    }

    return <>{children}</>;
}
