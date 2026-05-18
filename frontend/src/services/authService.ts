import api from "@/lib/axios";

export const loginUser = async (
  email: string,
  password: string
) => {
  const response = await api.post(
    "/auth/login",
    {
      email,
      password,
    }
  );

  return response.data;
};

export const signupUser = async (
  username: string,
  email: string,
  password: string
) => {
  const response = await api.post(
    "/auth/signup",
    {
      username,
      email,
      password,
    }
  );

  return response.data;
};
