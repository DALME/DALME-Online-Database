import * as yup from "yup";

import {
  attributeSchema,
  attributesFieldSchema,
  userAttributeSchema,
  groupAttributeSchema,
} from "@/schemas";

export const collectionAttributeSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  isPublished: yup.boolean().required(),
  isPrivate: yup.boolean().required(),
  useAsWorkset: yup.boolean().required(),
  owner: userAttributeSchema.default(null).nullable(),
  teamLink: groupAttributeSchema.default(null).nullable(),
  memberCount: yup.number().default(null).nullable(),
});

export const collectionSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  attributes: yup.array().of(attributeSchema).default(null).nullable(),
  useAsWorkset: yup.boolean().required(),
  isPublished: yup.boolean().required(),
  isPrivate: yup.boolean().required(),
  owner: userAttributeSchema.default(null).nullable(),
  teamLink: groupAttributeSchema.default(null).nullable(),
  creationTimestamp: yup.string().required(),
  modificationTimestamp: yup.string().required(),
  creationUser: userAttributeSchema.required(),
  modificationUser: userAttributeSchema.required(),
  memberCount: yup.number().default(null).nullable(),
  commentCount: yup.number().default(null).nullable(),
});

export const collectionsSchema = yup.array().of(collectionSchema);

// Field-level validation rules/schemas.
export const collectionFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  description: yup.string().nullable().required().label("Description"),
  permissions: yup
    .object()
    .shape({
      value: yup.number().required(),
      label: yup.string().required(),
    })
    .nullable()
    .required()
    .label("Permissions"),
  statTitle: yup.string().default(null).nullable().label("Status title"),
  statText: yup.string().default(null).nullable().label("Status text"),
  attributes: yup.array().of(attributesFieldSchema).default(null).nullable().label("Attributes"),
};

// Edit existing object schema.
// Transforms API data to the correct shape expected by the form.
export const collectionEditSchema = yup
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
    statTitle: yup.string().default(null).nullable(),
    statText: yup.string().default(null).nullable(),
    // NOTE: Just minimal validation here for the attributes. We apply the full
    // transform elsewhere, as it's very complex and better suits a function.
    attributes: yup.mixed(),
  })
  .camelCase()
  .transform((data) => {
    const { endpoint, hasLanding, isPublic, owner } = data;
    const attributes = {
      endpoint,
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
