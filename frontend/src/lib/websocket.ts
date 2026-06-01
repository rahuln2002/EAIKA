export const createWebSocket =
() => {

  const token =
    localStorage.getItem(
      "access_token"
    );

  return new WebSocket(
    `${import.meta.env.VITE_WS_URL}/ws/chat?token=${token}`
  );
};
