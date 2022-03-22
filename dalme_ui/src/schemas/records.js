import { isNil } from "ramda";
import * as yup from "yup";

import {
  agentsFieldSchema,
  attributesFieldSchema,
  foliosFieldSchema,
  creditsFieldSchema,
} from "@/schemas";

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
  attributes: yup.array().of(attributesFieldSchema).label("Attributes"),
  agents: yup.array().of(agentsFieldSchema).label("Agents"),
  folios: yup.array().of(foliosFieldSchema).label("Folios"),
  credits: yup.array().of(creditsFieldSchema).label("Credits"),
};

// Edit existing object schema.
export const recordEditSchema = null;

export const recordPostSchema = null;

export const recordPutSchema = null;
