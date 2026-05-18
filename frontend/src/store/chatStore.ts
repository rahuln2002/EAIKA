import { create } from "zustand";

interface Message {
  role: string;
  content: string;
}

interface ChatState {
  messages: Message[];

  addMessage: (
    message: Message
  ) => void;

  clearMessages: () => void;
}

export const useChatStore =
  create<ChatState>((set) => ({
    messages: [],

    addMessage: (message) =>
      set((state) => ({
        messages: [
          ...state.messages,
          message,
        ],
      })),

    clearMessages: () =>
      set({ messages: [] }),
  }));
