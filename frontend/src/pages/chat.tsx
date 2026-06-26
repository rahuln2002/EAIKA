import { useEffect, useRef, useState, useCallback } from "react";

import { createWebSocket } from "../lib/websocket";
import { logout } from "../lib/auth";

import { useChatStore } from "../store/chatStore";

export default function ChatPage() {
    // ===================================================
    // LOCAL STATE
    // ===================================================

    const [query, setQuery] = useState("");

    type Evaluation = {
        faithfulness: {
            faithfulness_score: number;
            matched_terms: number;
            total_terms: number;
        };

        hallucination: {
            hallucination_score: number;
            hallucinated_terms: string[];
        };

        relevancy: {
            avg_relevancy_score: number;
        };

        retrieval_metrics: {
            retrieved_chunks: number;
            avg_chunk_length: number;
        };
    };

    const [evaluation, setEvaluation] = useState<Evaluation | null>(null);

    const websocketRef = useRef<WebSocket | null>(null);

    const bottomRef = useRef<HTMLDivElement | null>(null);

    // ===================================================
    // GLOBAL STORE
    // ===================================================

    const {
        setChatId,

        messages,
        addMessage,

        streaming,
        setStreaming,

        resetChat,
    } = useChatStore();

    // ===================================================
    // AUTO SCROLL
    // ===================================================

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages, streaming]);

    // ===================================================
    // STREAM TOKEN APPENDER
    // ===================================================

    const addStreamingToken = (token: string) => {
        useChatStore.setState((state) => {
            const updated = [...state.messages];

            const last = updated[updated.length - 1];

            // =============================================
            // APPEND TO LAST ASSISTANT MESSAGE
            // =============================================

            if (last && last.role === "assistant") {
                last.content += token;
            } else {
                updated.push({
                    role: "assistant",
                    content: token,
                });
            }

            return {
                messages: updated,
            };
        });
    };

    // ===================================================
    // MESSAGE HANDLER
    // ===================================================

    const handleMessage = useCallback(
        (event: MessageEvent) => {
            try {
                const parsed = JSON.parse(event.data);

                if (parsed.type === "error") {
                    console.error(parsed.data);

                    if (
                        parsed.data === "Unauthorized" ||
                        parsed.data === "Token expired"
                    ) {
                        logout();
                        return;
                    }

                    setStreaming(false);

                    return;
                }

                if (parsed.type === "chat_id") {
                    setChatId(parsed.data);

                    return;
                }

                if (parsed.type === "evaluation") {
                    setEvaluation(parsed.data);

                    return;
                }

                if (parsed.type === "end") {
                    setStreaming(false);

                    return;
                }

                if (parsed.type === "token") {
                    addStreamingToken(parsed.data);
                }
            } catch (error) {
                console.error(error);
            }
        },
        [setChatId, setStreaming],
    );

    // ===================================================
    // WEBSOCKET SETUP
    // ===================================================

    const setupWebSocket = useCallback(() => {
        // prevent duplicate connections
        if (
            websocketRef.current &&
            websocketRef.current.readyState === WebSocket.OPEN
        ) {
            return;
        }

        const ws = createWebSocket();

        websocketRef.current = ws;

        ws.onmessage = handleMessage;

        ws.onclose = (event) => {
            setStreaming(false);

            if (event.code === 4001) {
                logout();
            }
        };

        ws.onerror = (error) => {
            console.error(error);

            setStreaming(false);
        };
    }, [handleMessage, setStreaming]);

    // ===================================================
    // INITIAL CONNECTION
    // ===================================================

    useEffect(() => {
        setupWebSocket();

        return () => {
            websocketRef.current?.close();
        };
    }, [setupWebSocket]);

    // ===================================================
    // SEND MESSAGE
    // ===================================================

    const handleSend = async () => {
        // ===============================================
        // VALIDATION
        // ===============================================

        if (!query.trim()) {
            return;
        }

        // ===============================================
        // RECONNECT IF CLOSED
        // ===============================================

        if (
            !websocketRef.current ||
            websocketRef.current.readyState !== WebSocket.OPEN
        ) {
            setupWebSocket();

            // wait briefly
            await new Promise((resolve) => setTimeout(resolve, 500));
        }

        // ===============================================
        // RESET SOURCES
        // ===============================================

        setEvaluation(null);

        // ===============================================
        // USER MESSAGE
        // ===============================================

        addMessage({
            role: "user",
            content: query,
        });

        // ===============================================
        // STREAMING
        // ===============================================

        setStreaming(true);

        if (websocketRef.current?.readyState === WebSocket.OPEN) {
            websocketRef.current.send(query);
        }

        setQuery("");
    };

    return (
        <div className="max-w-5xl mx-auto">
            {/* ========================================= */}
            {/* HEADER */}
            {/* ========================================= */}

            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Enterprise AI Chat</h1>

                <button
                    onClick={resetChat}
                    className="border px-4 py-2 rounded-lg"
                >
                    New Chat
                </button>
            </div>

            {/* ========================================= */}
            {/* CHAT WINDOW */}
            {/* ========================================= */}

            <div className="border rounded-xl p-4 h-75 overflow-y-auto mb-4">
                {/* ===================================== */}
                {/* MESSAGES */}
                {/* ===================================== */}

                {messages.map((message, idx) => (
                    <div
                        key={idx}
                        className={`mb-4 ${
                            message.role === "user" ? "text-right" : "text-left"
                        }`}
                    >
                        <div
                            className={`inline-block p-4 rounded-xl max-w-[80%] whitespace-pre-wrap ${
                                message.role === "user"
                                    ? "bg-black text-white"
                                    : "bg-gray-200 text-black"
                            }`}
                        >
                            {message.content}
                        </div>
                    </div>
                ))}

                {/* ===================================== */}
                {/* RESPONSE ANALYTICS */}
                {/* ===================================== */}

                {evaluation && (
                    <div className="mb-6 rounded-xl border bg-blue-50 p-4">
                        <h2 className="mb-3 text-lg font-semibold">
                            Response Analytics
                        </h2>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-sm text-gray-600">
                                    Faithfulness
                                </p>

                                <p className="font-bold text-green-600">
                                    {(
                                        evaluation.faithfulness
                                            .faithfulness_score * 100
                                    ).toFixed(1)}
                                    %
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-600">
                                    Hallucination
                                </p>

                                <p className="font-bold text-red-600">
                                    {(
                                        evaluation.hallucination
                                            .hallucination_score * 100
                                    ).toFixed(1)}
                                    %
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-600">
                                    Relevancy
                                </p>

                                <p className="font-bold text-blue-600">
                                    {(
                                        evaluation.relevancy
                                            .avg_relevancy_score * 100
                                    ).toFixed(1)}
                                    %
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-600">
                                    Retrieved Chunks
                                </p>

                                <p className="font-bold">
                                    {
                                        evaluation.retrieval_metrics
                                            .retrieved_chunks
                                    }
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                {/* ===================================== */}
                {/* STREAMING */}
                {/* ===================================== */}

                {streaming && (
                    <div className="text-gray-500 animate-pulse">
                        AI is typing...
                    </div>
                )}

                {/* ===================================== */}
                {/* AUTO SCROLL TARGET */}
                {/* ===================================== */}

                <div ref={bottomRef} />
            </div>

            {/* ========================================= */}
            {/* INPUT */}
            {/* ========================================= */}

            <div className="flex gap-2">
                <input
                    className="border p-4 flex-1 rounded-xl"
                    placeholder="Ask something..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !streaming) {
                            handleSend();
                        }
                    }}
                />

                <button
                    className="bg-black text-white px-6 rounded-xl disabled:opacity-50"
                    onClick={handleSend}
                    disabled={streaming}
                >
                    Send
                </button>
            </div>
        </div>
    );
}
