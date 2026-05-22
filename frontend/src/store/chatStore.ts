import { create } from "zustand";


// =====================================================
// TYPES
// =====================================================

export interface Message {

  role: string;

  content: string;
}


export interface Source {

  chunk_id: number;

  document_id: number;

  citation: string;

  content: string;
}


// =====================================================
// STORE
// =====================================================

interface ChatState {

  // ================================================
  // ACTIVE CHAT
  // ================================================

  chatId: number | null;

  setChatId: (
    chatId: number
  ) => void;

  // ================================================
  // MESSAGES
  // ================================================

  messages: Message[];

  addMessage: (
    message: Message
  ) => void;

  setMessages: (
    messages: Message[]
  ) => void;

  clearMessages: () => void;

  // ================================================
  // SOURCES
  // ================================================

  sources: Source[];

  setSources: (
    sources: Source[]
  ) => void;

  clearSources: () => void;

  // ================================================
  // LOADING
  // ================================================

  loading: boolean;

  setLoading: (
    loading: boolean
  ) => void;

  // ================================================
  // STREAMING
  // ================================================

  streaming: boolean;

  setStreaming: (
    streaming: boolean
  ) => void;

  // ================================================
  // RESET SESSION
  // ================================================

  resetChat: () => void;
}


// =====================================================
// STORE IMPLEMENTATION
// =====================================================

export const useChatStore =
  create<ChatState>((set) => ({

    // ==============================================
    // ACTIVE CHAT
    // ==============================================

    chatId: null,

    setChatId: (chatId) =>
      set({
        chatId,
      }),

    // ==============================================
    // MESSAGES
    // ==============================================

    messages: [],

    addMessage: (message) =>
      set((state) => ({
        messages: [
          ...state.messages,
          message,
        ],
      })),

    setMessages: (messages) =>
      set({
        messages,
      }),

    clearMessages: () =>
      set({
        messages: [],
      }),

    // ==============================================
    // SOURCES
    // ==============================================

    sources: [],

    setSources: (sources) =>
      set({
        sources,
      }),

    clearSources: () =>
      set({
        sources: [],
      }),

    // ==============================================
    // LOADING
    // ==============================================

    loading: false,

    setLoading: (loading) =>
      set({
        loading,
      }),

    // ==============================================
    // STREAMING
    // ==============================================

    streaming: false,

    setStreaming: (streaming) =>
      set({
        streaming,
      }),

    // ==============================================
    // RESET SESSION
    // ==============================================

    resetChat: () =>
      set({
        chatId: null,
        messages: [],
        sources: [],
        loading: false,
        streaming: false,
      }),
  }));
