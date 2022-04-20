import * as yup from "yup";

import { attributesFieldSchema } from "@/schemas";

export const bibliographyTypeOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({ value: yup.number().required(), label: yup.string().required() })
    .transform((data) => ({ value: data.id, label: data.name })),
);

// Field-level validation rules/schemas.
export const bibliographyFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  shortName: yup.string().nullable().required().label("Short name"),
  type: yup
    .object()
    .shape({
      value: yup.number().nullable().required(),
    })
    .nullable()
    .required()
    .label("Bibliography type"),
  primaryDataset: yup
    .object()
    .shape({ value: yup.string().uuid().nullable() })
    .nullable()
    .required() // TODO: Is it?
    .label("Primary dataset"),
  sets: yup
    .array()
    .of(yup.object().shape({ value: yup.string().uuid().nullable() }))
    .nullable()
    .label("Sets"),
  attributes: yup
    .array()
    .of(attributesFieldSchema)
    .required()
    .label("Attributes"),
};

// Edit existing object schema.
// Transforms API data to the correct shape expected by the form.
export const bibliographyEditSchema = null;
