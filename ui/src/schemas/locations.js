import * as yup from "yup";

import { attributeSchema } from "@/schemas";

export const locationSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  locationType: yup.string().required(),
  attributes: yup.array().of(attributeSchema).required(),
});

export const locationListSchema = yup.array().of(locationSchema);
