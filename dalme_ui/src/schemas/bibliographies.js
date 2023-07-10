import camelcaseKeys from "camelcase-keys";
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
  attributes: yup.array().of(attributesFieldSchema).required().label("Attributes"),
};

// Edit existing object schema.
// Transforms API data to the correct shape expected by the form.
export const bibliographyEditSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    shortName: yup.string().required(),
    type: yup
      .object()
      .shape({ value: yup.number().required(), label: yup.string().required() })
      .required(),
    primaryDataset: yup
      .object()
      .shape({
        value: yup.string().uuid().nullable(),
        label: yup.string().required(),
      })
      .default(null)
      .nullable(),
    sets: yup
      .array()
      .of(
        yup.object().shape({
          value: yup.string().uuid().nullable(),
          label: yup.string().required(),
        }),
      )
      .default(null)
      .nullable(),
    attributes: yup.mixed(),
  })
  .camelCase()
  .transform((data) => ({
    ...data,
    type: {
      value: data.type.id,
      label: data.type.name,
    },
    primaryDataset: {
      value: data.primaryDataset.id,
      label: data.primaryDataset.name,
    },
    sets: data.sets.map((item) => ({ value: item.id, label: item.name })),
    // TODO: Remove ALL camelcase hackage when we sort out the API renderer.
    // Until then, we camelize here because we run a function not a schema to
    // normalize the attributes so we can't call on yup to camelCase the data.
    attributes: camelcaseKeys(data.attributes),
  }));
