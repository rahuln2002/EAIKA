import { useState } from "react";

import axios from "axios";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function SummarizePage() {
    const [text, setText] = useState("");

    const [summary, setSummary] = useState("");

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const handleSummarize = async () => {
        if (!text.trim()) {
            setError("Please enter a document to summarize.");
            return;
        }

        try {
            setLoading(true);
            setError("");
            setSummary("");

            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/summarization/`,
                null,
                {
                    params: { text },
                },
            );

            setSummary(response.data.final_summary ?? "");
        } catch (err) {
            console.error("Summarization failed:", err);
            setError("Failed to summarize the document. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6">AI Summarization</h1>

            <textarea
                className="border p-4 w-full h-64 rounded-lg mb-4"
                placeholder="Paste long document..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                disabled={loading}
            />

            <button
                className="px-6 py-3 rounded-lg bg-black text-white
                    disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={handleSummarize}
                disabled={loading || !text.trim()}
            >
                {loading ? "Summarizing..." : "Summarize"}
            </button>

            {error && (
                <p className="mt-4 text-red-600" role="alert">
                    {error}
                </p>
            )}

            {summary && (
                <div className="mt-8 border rounded-lg p-6">
                    <h2 className="text-2xl font-bold mb-4">
                        Executive Summary
                    </h2>

                    <div className="prose prose-sm max-w-none wrap-break-word">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {summary}
                        </ReactMarkdown>
                    </div>
                </div>
            )}
        </div>
    );
}
