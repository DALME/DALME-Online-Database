import { isNil } from "ramda";
import * as yup from "yup";

import { attributeOptionSchema } from "@/schemas";

export const recordFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  shortName: yup.string().nullable().required().label("Short name"),
  // TODO: sets
  hasInventory: yup
    .boolean()
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : Boolean(option.value)))
    .label("List"),
  parent: yup.string().uuid().default(null).nullable().label("Parent"),
  attributes: yup
    .array()
    .of(attributeOptionSchema)
    .required()
    .label("Attributes"),
  // TODO: pages/folios
};

export const recordPostSchema = null;

export const recordPutSchema = null;
