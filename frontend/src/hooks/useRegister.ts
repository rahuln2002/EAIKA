import { useMutation } from "@tanstack/react-query";

import { signupUser } from "@/services/authService";

export const useRegister = () => {
  return useMutation({
    mutationFn: ({
      username,
      email,
      password,
    }: {
      username: string;
      email: string;
      password: string;
    }) =>
      signupUser(
        username,
        email,
        password
      ),
  });
};
