import * as yup from "yup";

import { attributeOptionSchema } from "@/schemas";

// Field-level validation rules/schemas.
export const archiveFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  shortName: yup.string().nullable().required().label("Short name"),
  sets: yup
    .array()
    .of(yup.object().shape({ value: yup.string().uuid().nullable() }))
    .nullable()
    .label("Sets"),
  attributes: yup
    .array()
    .of(attributeOptionSchema)
    .required()
    .label("Attributes"),
};

// Full object schema.
// TODO: Port over from schemas/sources.

// Edit existing object schema.
export const archiveEditSchema = null;

// API submit schemas.
export const archivePostSchema = null;

export const archivePutSchema = null;
