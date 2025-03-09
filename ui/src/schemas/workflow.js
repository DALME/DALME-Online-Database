import * as yup from "yup";
import { timeStampSchema, userAttributeSchema } from "@/schemas";

export const logEventSchema = yup.object().shape({
  event: yup.string().required(),
  id: yup.number().required(),
  timestamp: timeStampSchema.required(),
  user: userAttributeSchema.required(),
});

export const workflowSchema = yup.object().shape({
  helpFlag: yup.boolean().required(),
  isPublic: yup.boolean().required(),
  wfStatus: yup.number().required(),
  stage: yup.number().default(null).nullable(),
  ingestionDone: yup.boolean().required(),
  transcriptionDone: yup.boolean().required(),
  markupDone: yup.boolean().required(),
  reviewDone: yup.boolean().required(),
  parsingDone: yup.boolean().default(null).nullable(),
  lastModified: timeStampSchema.required(),
  lastUser: userAttributeSchema.required(),
  status: yup.string().required(),
  workLog: yup.array().of(logEventSchema).default(null).nullable(),
});
