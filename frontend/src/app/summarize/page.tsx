"use client";

import { useState } from "react";

import axios from "axios";

export default function SummarizePage() {
  const [text, setText] =
    useState("");

  const [summary, setSummary] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleSummarize =
    async () => {
      try {
        setLoading(true);

        const response =
          await axios.post(
            "http://localhost:8000/api/v1/summarization",
            null,
            {
              params: { text },
            }
          );

        setSummary(
          response.data.final_summary
        );

      } catch (error) {
        console.error(error);

      } finally {
        setLoading(false);
      }
    };

  return (
    <div className="max-w-4xl mx-auto p-10">
      <h1 className="text-3xl font-bold mb-6">
        AI Summarization
      </h1>

      <textarea
        className="border p-4 w-full h-64 rounded-lg mb-4"
        placeholder="Paste long document..."
        value={text}
        onChange={(e) =>
          setText(e.target.value)
        }
      />

      <button
        className="bg-black text-white px-6 py-3 rounded-lg"
        onClick={handleSummarize}
        disabled={loading}
      >
        {loading
          ? "Summarizing..."
          : "Summarize"}
      </button>

      {summary && (
        <div className="mt-8 border rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">
            Executive Summary
          </h2>

          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}
