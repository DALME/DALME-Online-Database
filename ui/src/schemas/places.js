import { isNil } from "ramda";
import * as yup from "yup";

import { timeStampSchema } from "@/schemas";

export const placeSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  attributeIds: yup
    .array()
    .default([])
    .required()
    .transform((value) => (isNil(value) ? [] : value)),
  locationId: yup.string().uuid().default(null).nullable(),
  commentCount: yup.number().required(),
  attestationCount: yup.number().default(null).nullable(),
  recordAttestationCount: yup.number().default(null).nullable(),
  creationTimestamp: timeStampSchema.required(),
  creationUserId: yup.number().required(),
  modificationTimestamp: timeStampSchema.required(),
  modificationUserId: yup.number().required(),
});

export const placeListSchema = yup.array().of(placeSchema);
