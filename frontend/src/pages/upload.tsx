"use client";

import { useState } from "react";

import toast from "react-hot-toast";

import { useUploadDocument } from "../hooks/useUploadDocument";

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null);

    const uploadMutation = useUploadDocument();

    const handleUpload = async () => {
        if (!file) {
            toast.error("Please select a file.");

            return;
        }

        try {
            await uploadMutation.mutateAsync(file);

            toast.success("Upload successful!");

            setFile(null);
        } catch {
            toast.error("Upload failed.");
        }
    };

    return (
        <div className="max-w-xl mx-auto p-10">
            <h1 className="text-3xl font-bold mb-6">Upload Document</h1>

            <div className="border rounded-lg p-6">
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="mb-4"
                />

                <button
                    className="bg-black text-white px-6 py-3 rounded"
                    onClick={handleUpload}
                    disabled={uploadMutation.isPending}
                >
                    {uploadMutation.isPending ? "Uploading..." : "Upload"}
                </button>
            </div>
        </div>
    );
}
