import * as yup from "yup";

import { attachmentSchema, timeStampSchema, userAttributeSchema } from "@/schemas";

export const rightsSchema = yup
  .object()
  .shape({
    attachments: attachmentSchema.default(null).nullable(),
    commentCount: yup.number().default(null).nullable(),
    creationTimestamp: timeStampSchema.required(),
    creationUser: userAttributeSchema.required(),
    id: yup.string().uuid().required(),
    licence: yup.string().default(null).nullable(),
    modificationTimestamp: timeStampSchema.required(),
    modificationUser: userAttributeSchema.required(),
    name: yup.string().required(),
    noticeDisplay: yup.boolean().required(),
    publicDisplay: yup.boolean().required(),
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
  })
  .camelCase();

export const rightsListSchema = yup.array().of(rightsSchema);
