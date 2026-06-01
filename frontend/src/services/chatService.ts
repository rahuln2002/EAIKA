import api from "../lib/axios";

export const sendMessage = async (
  query: string,
  chatId?: number
) => {
  const response = await api.post(
    `/chat?query=${query}${
      chatId
        ? `&chat_id=${chatId}`
        : ""
    }`
  );

  return response.data;
};
