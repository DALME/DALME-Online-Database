import * as yup from "yup";

import { attributesFieldSchema } from "@/schemas";

// Field-level validation rules/schemas.
export const datasetFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  description: yup.string().nullable().required().label("Description"),
  permissions: yup.string().default(null).nullable().label("Permissions"),
  datasetUsergroup: yup
    .object()
    .shape({ value: yup.number().required().label("Dataset group") })
    .nullable()
    .required()
    .label("Dataset group"),
  attributes: yup
    .array()
    .of(attributesFieldSchema)
    .default(null)
    .nullable()
    .label("Attributes"),
};

// Edit existing object schema.
// Transforms API data to the correct shape expected by the form.
export const datasetEditSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    description: yup.string().required(),
    permissions: yup
      .object()
      .shape({
        value: yup.number().required(),
        label: yup.string().required(),
      })
      .required(),
    datasetUsergroup: yup
      .object()
      .shape({
        value: yup.number().required(),
        label: yup.string().required(),
      })
      .required(),
    // NOTE: Just minimal validation here for the attributes. We apply the full
    // transform elsewhere, as it's very complex and better suits a function.
    attributes: yup.mixed(),
  })
  .camelCase()
  .transform((data) => {
    const { endpoint, owner } = data;
    const attributes = {
      endpoint,
      owner: { value: owner.id, label: owner.full_name },
    };

    return {
      ...data,
      attributes,
      permissions: {
        value: data.permissions.id,
        label: data.permissions.name,
      },
      datasetUsergroup: {
        value: data.datasetUsergroup.id,
        label: data.datasetUsergroup.name,
      },
    };
  });
