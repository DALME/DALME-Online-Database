import { isNil } from "ramda";
import * as yup from "yup";

import { attributeOptionSchema } from "@/schemas";

export const recordFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  shortName: yup.string().nullable().required().label("Short name"),
  hasInventory: yup
    .object()
    .shape({
      value: yup
        .boolean()
        .nullable()
        .required()
        .transform((option) => (isNil(option) ? null : Boolean(option.value))),
    })
    .nullable()
    .required()
    .label("List"),
  parent: yup
    .object()
    .shape({ value: yup.string().uuid().nullable() })
    .nullable()
    .label("Parent"),
  sets: yup
    .array()
    .of(yup.object().shape({ value: yup.string().uuid().nullable() }))
    .nullable()
    .label("Sets"),
  folios: yup
    .array()
    .of(yup.object().shape({ value: yup.string().uuid().nullable() }))
    .nullable()
    .label("Folios"),
  attributes: yup
    .array()
    .of(attributeOptionSchema)
    .required()
    .label("Attributes"),
};

// Edit existing object schema.
export const recordEditSchema = null;

export const recordPostSchema = null;

export const recordPutSchema = null;
