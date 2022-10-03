import * as yup from "yup";
import { attachmentSchema, userRefSchema } from "@/schemas";

export const rightsListSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.string().uuid().required(),
      name: yup.string().required(),
      rights: yup.string().required(),
      rightsHolder: yup.string().required(),
      rightsNotice: yup.string().default(null).nullable(),
      rightsStatus: yup
        .object()
        .shape({
          id: yup.number().required(),
          name: yup.string().required(),
        })
        .required(),
      publicDisplay: yup.boolean().required(),
      noticeDisplay: yup.boolean().required(),
      commentCount: yup.number().default(null).nullable(),
      licence: yup.string().default(null).nullable(),
      creationTimestamp: yup.string().required(),
      creationUser: userRefSchema.required(),
      modificationTimestamp: yup.string().required(),
      modificationUser: userRefSchema.required(),
      attachments: attachmentSchema.default(null).nullable(),
    })
    .camelCase(),
);
