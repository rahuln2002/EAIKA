"use client";

import { useState } from "react";

import { uploadDocument } from "@/services/uploadService";

export default function UploadPage() {
  const [file, setFile] =
    useState<File | null>(null);

  const handleUpload =
    async () => {
      if (!file) return;

      try {
        await uploadDocument(file);

        alert(
          "Upload successful!"
        );

      } catch {
        alert("Upload failed.");
      }
    };

  return (
    <div className="p-10">
      <h1 className="text-2xl mb-4">
        Upload Document
      </h1>

      <input
        type="file"
        onChange={(e) =>
          setFile(
            e.target.files?.[0] || null
          )
        }
      />

      <button
        className="bg-black text-white p-2 ml-2"
        onClick={handleUpload}
      >
        Upload
      </button>
    </div>
  );
}
