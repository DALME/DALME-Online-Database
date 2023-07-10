import camelcaseKeys from "camelcase-keys";
import * as yup from "yup";

import { attributesFieldSchema } from "@/schemas";

// Field-level validation rules/schemas.
export const archivalFileFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  shortName: yup.string().nullable().required().label("Short name"),
  parent: yup
    .object()
    .shape({ value: yup.string().uuid().nullable() })
    .default(null)
    .nullable()
    .label("Parent"),
  primaryDataset: yup
    .object()
    .shape({ value: yup.string().uuid().nullable() })
    .default(null)
    .nullable()
    .label("Primary dataset"),
  attributes: yup.array().of(attributesFieldSchema).required().label("Attributes"),
};

// Edit existing object schema.
// Transforms API data to the correct shape expected by the form.
export const archivalFileEditSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    shortName: yup.string().required(),
    parent: yup
      .object()
      .shape({
        value: yup.string().uuid().required(),
        label: yup.string().required(),
      })
      .default(null)
      .nullable(),
    primaryDataset: yup
      .object()
      .shape({
        value: yup.string().uuid().required(),
        label: yup.string().required(),
      })
      .default(null)
      .nullable(),
    // NOTE: Just minimal validation here for the attributes. We apply the full
    // transform elsewhere, as it's very complex and better suits a function.
    attributes: yup.mixed(),
  })
  .camelCase()
  .transform((data) => ({
    ...data,
    parent: { value: data.parent.id, label: data.parent.name },
    primaryDataset: {
      value: data.primaryDataset.id,
      label: data.primaryDataset.name,
    },
    // TODO: Remove ALL camelcase hackage when we sort out the API renderer.
    // Until then, we camelize here because we run a function not a schema to
    // normalize the attributes so we can't call on yup to camelCase the data.
    attributes: camelcaseKeys(data.attributes),
  }));
