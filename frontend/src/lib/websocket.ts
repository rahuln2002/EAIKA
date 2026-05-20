export const createWebSocket = () => {

  const token = localStorage.getItem(
    "access_token"
  );

  return new WebSocket(
    `ws://localhost:8000/api/v1/ws/chat?token=${token}`
  );
};
