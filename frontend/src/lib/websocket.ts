export const createWebSocket = () => {
  return new WebSocket(
    "ws://localhost:8000/api/v1/ws/chat"
  );
};
