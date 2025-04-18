import * as yup from "yup";

import { attributeSchema, locationSchema, timeStampSchema, userAttributeSchema } from "@/schemas";

export const placeSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  attributes: yup.array().of(attributeSchema).required(),
  location: locationSchema.default(null).nullable(),
  commentCount: yup.number().required(),
  attestationCount: yup.number().default(null).nullable(),
  recordAttestationCount: yup.number().default(null).nullable(),
  creationTimestamp: timeStampSchema.required(),
  creationUser: userAttributeSchema.required(),
  modificationTimestamp: timeStampSchema.required(),
  modificationUser: userAttributeSchema.required(),
});

export const placeListSchema = yup.array().of(placeSchema);
