export const createWebSocket = () => {

  const token =
    localStorage.getItem(
      "access_token"
    );

  // ============================================
  // BASE WS URL
  // ============================================

  const baseUrl =
    process.env
      .NEXT_PUBLIC_WS_URL;

  if (!baseUrl) {
    throw new Error(
      "NEXT_PUBLIC_WS_URL is not defined"
    );
  }

  // ============================================
  // CREATE WEBSOCKET
  // ============================================

  return new WebSocket(
    `${baseUrl}/api/v1/ws/chat?token=${token}`
  );
};
