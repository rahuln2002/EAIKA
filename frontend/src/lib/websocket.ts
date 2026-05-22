export const createWebSocket = (
  chatId?: number | null
) => {

  const token =
    localStorage.getItem(
      "access_token"
    );

  let url =
    `${process.env.NEXT_PUBLIC_WS_URL}/ws/chat?token=${token}`;

  if (chatId) {

    url += `&chat_id=${chatId}`;
  }

  return new WebSocket(url);
};
