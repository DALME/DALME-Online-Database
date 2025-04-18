import * as yup from "yup";

import { tenantSchema } from "@/schemas";

export const groupSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
  description: yup.string().required(),
  tenant: tenantSchema,
});

export const groupAttributeSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
  groupType: yup.string().required(),
  description: yup.string().required(),
});

export const groupOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().required(),
    })
    .transform((value) => ({
      label: value.name,
      value: value.id,
      caption: value.description,
    })),
);
