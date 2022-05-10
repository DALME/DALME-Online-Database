import * as yup from "yup";

import { attributesFieldSchema } from "@/schemas";

// Field-level validation rules/schemas.
export const corpusFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  description: yup.string().nullable().required().label("Description"),
  permissions: yup.string().nullable().required().label("Permissions"),
  attributes: yup
    .array()
    .of(attributesFieldSchema)
    .default(null)
    .nullable()
    .label("Attributes"),
};

// Edit existing object schema.
// Transforms API data to the correct shape expected by the form.
export const corpusEditSchema = yup
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
    // NOTE: Just minimal validation here for the attributes. We apply the full
    // transform elsewhere, as it's very complex and better suits a function.
    attributes: yup.mixed(),
  })
  .camelCase()
  .transform((data) => {
    const { endpoint, hasLanding, isPublic, owner } = data;
    const attributes = {
      endpoint: endpoint,
      hasLanding: { value: hasLanding, label: hasLanding ? "True" : "False" },
      isPublic: { value: isPublic, label: isPublic ? "True" : "False" },
      owner: { value: owner.id, label: owner.full_name },
    };
    return {
      ...data,
      attributes,
      permissions: {
        value: data.permissions.id,
        label: data.permissions.name,
      },
    };
  });
