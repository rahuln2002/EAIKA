import { useMutation } from "@tanstack/react-query";

import { uploadDocument } from "@/services/uploadService";

export const useUploadDocument =
  () => {
    return useMutation({
      mutationFn: (file: File) =>
        uploadDocument(file),
    });
  };
