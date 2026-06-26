import { getToken } from "./auth";

export const createWebSocket =
() => {

  const token = getToken();

  return new WebSocket(
    `${import.meta.env.VITE_WS_URL}/ws/chat?token=${token}`
  );
};
