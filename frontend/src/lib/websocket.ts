export const createWebSocket =
() => {

  const token =
    localStorage.getItem(
      "access_token"
    );

  return new WebSocket(
    `${process.env.NEXT_PUBLIC_WS_URL}/ws/chat?token=${token}`
  );
};
