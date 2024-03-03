import * as yup from "yup";

export const transcriptionsFieldSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  transcription: yup.string().required(),
  author: yup.string().required(),
  version: yup.number().required(),
});
