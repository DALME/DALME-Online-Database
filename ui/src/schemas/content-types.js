import * as yup from "yup";

import { attributeTypesListSchema } from "@/schemas";

export const baseContentTypeSchema = yup.object().shape({
  id: yup.number().required(),
  appLabel: yup.string().required(),
  model: yup.string().required(),
});

export const contentTypeSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
  description: yup.string().required(),
  isAbstract: yup.boolean().required(),
  attributeTypes: attributeTypesListSchema.nullable().required(),
  parent: yup.number().nullable().default(null),
  canView: yup.boolean().required(),
  canEdit: yup.boolean().required(),
  canDelete: yup.boolean().required(),
  canAdd: yup.boolean().required(),
  canRemove: yup.boolean().required(),
});

export const contentTypesListSchema = yup.array().of(contentTypeSchema);
