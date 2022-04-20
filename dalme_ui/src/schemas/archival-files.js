import * as yup from "yup";

import { attributesFieldSchema } from "@/schemas";

// Field-level validation rules/schemas.
export const archivalFileFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  shortName: yup.string().nullable().required().label("Short name"),
  parent: yup
    .object() // TODO: required?
    .shape({ value: yup.string().uuid().nullable() })
    .label("Parent"),
  primaryDataset: yup
    .object() // TODO: required?
    .shape({ value: yup.string().uuid().nullable() })
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
export const archivalFileEditSchema = null;
