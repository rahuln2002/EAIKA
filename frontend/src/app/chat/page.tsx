"use client";

import { useEffect } from "react";
import { useRef } from "react";
import { useState } from "react";

import { createWebSocket } from "@/lib/websocket";

interface Message {
  role: string;
  content: string;
}

export default function ChatPage() {
  const [query, setQuery] =
    useState("");

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [streaming, setStreaming] =
    useState(false);

  const websocketRef =
    useRef<WebSocket | null>(null);

  const [sources, setSources] =
    useState<any[]>([]);

  // =====================================================
  // CONNECT WEBSOCKET
  // =====================================================

  useEffect(() => {
    const ws = createWebSocket();

    websocketRef.current = ws;

    ws.onmessage = (event) => {
      const token = event.data;

      if (token === "[END]") {
        setStreaming(false);

        return;
      }

      setMessages((prev) => {
        const updated = [...prev];

        const lastMessage =
          updated[
            updated.length - 1
          ];

        // =============================================
        // APPEND TOKENS TO ASSISTANT MESSAGE
        // =============================================

        if (
          lastMessage &&
          lastMessage.role ===
            "assistant"
        ) {
          lastMessage.content += token;

        } else {
          updated.push({
            role: "assistant",
            content: token,
          });
        }

        return [...updated];
      });
    };

    return () => {
      ws.close();
    };
  }, []);

  // =====================================================
  // SEND MESSAGE
  // =====================================================

  const handleSend = async () => {
    if (
      !query.trim() ||
      !websocketRef.current
    ) {
      return;
    }

    // ===============================================
    // ADD USER MESSAGE
    // ===============================================

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: query,
      },
    ]);

    setStreaming(true);

    websocketRef.current.send(query);

    setQuery("");
  };

  setSources(
    response.sources || []
  );

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">
        Enterprise AI Chat
      </h1>

      {/* ========================================= */}
      {/* CHAT WINDOW */}
      {/* ========================================= */}

      <div className="border rounded-lg p-4 h-[500px] overflow-y-auto mb-4">
        {messages.map(
          (message, idx) => (
            <div
              key={idx}
              className={`mb-4 ${
                message.role ===
                "user"
                  ? "text-right"
                  : "text-left"
              }`}
            >
              <div
                className={`inline-block p-3 rounded-lg max-w-[80%] ${
                  message.role ===
                  "user"
                    ? "bg-black text-white"
                    : "bg-gray-200 text-black"
                }`}
              >
                {message.content}
              </div>
            </div>
          )
        )}

        {/* ===================================== */}
        {/* TYPING INDICATOR */}
        {/* ===================================== */}

        {streaming && (
          <div className="text-gray-500 animate-pulse">
            AI is typing...
          </div>
        )}
      </div>

      {/* ========================================= */}
      {/* INPUT AREA */}
      {/* ========================================= */}

      <div className="flex gap-2">
        <input
          className="border p-3 flex-1 rounded-lg"
          placeholder="Ask something..."
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
        />

        <button
          className="bg-black text-white px-6 rounded-lg"
          onClick={handleSend}
          disabled={streaming}
        >
          Send
        </button>
      </div>
    </div>
  );
}
