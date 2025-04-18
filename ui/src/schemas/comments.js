import * as yup from "yup";

import { timeStampSchema, userAttributeSchema } from "@/schemas";

export const commentSchema = yup.object().shape({
  body: yup.string().required(),
  creationUser: userAttributeSchema.required(),
  creationTimestamp: timeStampSchema.required(),
});

export const commentsSchema = yup.object().shape({
  data: yup.array().of(commentSchema),
  filtered: yup.number().nullable(),
  count: yup.number().required(),
});

export const commentPayloadSchema = yup.object().shape({
  body: yup.string().required(),
  model: yup.string().required(),
  object: yup.lazy((val) => (typeof val === "number" ? yup.number() : yup.string())),
});
