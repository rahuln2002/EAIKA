import { useEffect, useState } from "react";

import toast from "react-hot-toast";

import { useNavigate } from "react-router-dom";

import axios from "axios";

import { useUploadDocument } from "../hooks/useUploadDocument";
import { getUploadStatus } from "../services/uploadService";

import { logout } from "../lib/auth";

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null);

    const [documentId, setDocumentId] = useState<number | null>(null);

    const [progress, setProgress] = useState(0);

    const [status, setStatus] = useState("");

    const uploadMutation = useUploadDocument();

    const navigate = useNavigate();

    // ===================================================
    // POLL UPLOAD STATUS
    // ===================================================

    useEffect(() => {
        if (!documentId) return;

        const interval = setInterval(async () => {
            try {
                const data = await getUploadStatus(documentId);

                setProgress(data.progress);

                setStatus(data.status);

                if (data.progress >= 100) {
                    clearInterval(interval);

                    toast.success("Upload completed successfully!");

                    setTimeout(() => {
                        navigate("/chat");
                    }, 500);
                }
            } catch (error: unknown) {
                if (
                    axios.isAxiosError(error) &&
                    error.response?.status === 401
                ) {
                    logout();
                    return;
                }

                toast.error("Unable to fetch upload status.");
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [documentId, navigate]);

    // ===================================================
    // HANDLE UPLOAD
    // ===================================================

    const handleUpload = async () => {
        if (!file) {
            toast.error("Please select a file.");

            return;
        }

        try {
            const response = await uploadMutation.mutateAsync(file);

            setDocumentId(response.document_id);
        } catch (error) {
            console.error(error);

            toast.error("Upload failed.");
        }
    };

    return (
        <div className="max-w-xl mx-auto">
            <h1 className="text-3xl font-bold mb-6">Upload Document</h1>

            <div className="border rounded-lg p-6 space-y-5">
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                />

                <button
                    onClick={handleUpload}
                    disabled={uploadMutation.isPending || documentId !== null}
                    className="bg-black text-white px-6 py-3 rounded disabled:opacity-50"
                >
                    {uploadMutation.isPending ? "Starting Upload..." : "Upload"}
                </button>

                {documentId && (
                    <div className="space-y-3">
                        <div className="flex justify-between text-sm">
                            <span>{status}</span>

                            <span>{progress}%</span>
                        </div>

                        <div className="w-full bg-gray-200 rounded-full h-3">
                            <div
                                className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                                style={{
                                    width: `${progress}%`,
                                }}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
