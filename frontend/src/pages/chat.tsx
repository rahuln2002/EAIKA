"use client";

import { useEffect, useRef, useState } from "react";

import { createWebSocket } from "../lib/websocket";

import { useChatStore } from "../store/chatStore";

export default function ChatPage() {
    // ===================================================
    // LOCAL STATE
    // ===================================================

    const [query, setQuery] = useState("");

    const websocketRef = useRef<WebSocket | null>(null);

    const bottomRef = useRef<HTMLDivElement | null>(null);

    // ===================================================
    // GLOBAL STORE
    // ===================================================

    const {
        setChatId,

        messages,
        addMessage,

        sources,
        setSources,

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

    const handleMessage = (event: MessageEvent) => {
        try {
            const parsed = JSON.parse(event.data);

            // =============================================
            // ERROR
            // =============================================

            if (parsed.type === "error") {
                console.error(parsed.data);

                setStreaming(false);

                return;
            }

            // =============================================
            // CHAT ID
            // =============================================

            if (parsed.type === "chat_id") {
                setChatId(parsed.data);

                return;
            }

            // =============================================
            // SOURCES
            // =============================================

            if (parsed.type === "sources") {
                setSources(parsed.data);

                return;
            }

            // =============================================
            // END STREAM
            // =============================================

            if (parsed.type === "end") {
                setStreaming(false);

                return;
            }

            // =============================================
            // TOKEN
            // =============================================

            if (parsed.type === "token") {
                addStreamingToken(parsed.data);
            }
        } catch (error) {
            console.error(error);
        }
    };

    // ===================================================
    // WEBSOCKET SETUP
    // ===================================================

    const setupWebSocket = () => {
        const ws = createWebSocket();

        websocketRef.current = ws;

        // ===============================================
        // EVENTS
        // ===============================================

        ws.onmessage = handleMessage;

        ws.onclose = () => {
            console.log("WebSocket disconnected");

            setStreaming(false);
        };

        ws.onerror = (error) => {
            console.error(error);

            setStreaming(false);
        };
    };

    // ===================================================
    // INITIAL CONNECTION
    // ===================================================

    useEffect(() => {
        setupWebSocket();

        return () => {
            websocketRef.current?.close();
        };
    }, []);

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

        setSources([]);

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

        websocketRef.current?.send(query);

        setQuery("");
    };

    return (
        <div className="max-w-5xl mx-auto p-6">
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

            <div className="border rounded-xl p-4 h-150 overflow-y-auto mb-4">
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
                {/* SOURCES */}
                {/* ===================================== */}

                {sources.length > 0 && (
                    <div className="border rounded-xl p-4 mb-4 bg-gray-50">
                        <h2 className="text-xl font-bold mb-4">Sources</h2>

                        {sources.map((source, idx) => (
                            <div key={idx} className="mb-4 border-b pb-2">
                                <div className="font-semibold">
                                    {source.citation || `Source ${idx + 1}`}
                                </div>

                                <div className="text-sm text-gray-500">
                                    Document ID: {source.document_id}
                                </div>

                                <div className="mt-2 text-sm whitespace-pre-wrap">
                                    {source.content}
                                </div>
                            </div>
                        ))}
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
