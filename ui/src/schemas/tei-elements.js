import * as yup from "yup";
import { OptionListSchema } from "@/schemas";

export const ElementTagAttributeSchema = yup.object().shape({
  label: yup.string().required(),
  value: yup.string().required(),
  kind: yup.string().nullable(),
  description: yup.string().nullable(),
  required: yup.boolean().required(),
  editable: yup.boolean().required(),
  default: yup.string().nullable(),
  options: OptionListSchema.nullable(),
});

export const ElementTagAttributeListSchema = yup.array().of(ElementTagAttributeSchema);

export const ElementTagSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  element: yup.string().uuid().required(),
  name: yup.string().required(),
  kind: yup.string().required(),
  placeholder: yup.string().nullable(),
  parent: yup.string().uuid().nullable(),
  icon: yup.string().nullable(),
  attributes: ElementTagAttributeListSchema,
});

export const ElementTagListSchema = yup.array().of(ElementTagSchema);

export const ElementSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  label: yup.string().required(),
  section: yup.string().required(),
  description: yup.string().required(),
  kbReference: yup.string().required(),
  compound: yup.boolean().required(),
  icon: yup.string().nullable(),
  tags: yup
    .array()
    .transform((tags) => tags.map((tag) => tag.id))
    .required(),
});

export const ElementListSchema = yup.array().of(ElementSchema);

export const ElementSetSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  label: yup.string().required(),
  description: yup.string().required(),
  project: yup.string().nullable(),
  isDefault: yup.boolean().required(),
  members: yup
    .array()
    .of(
      yup.object().shape({
        element: yup.string().uuid().required(),
        inContextMenu: yup.boolean().required(),
        inToolbar: yup.boolean().required(),
        shortcut: yup.string().nullable(),
      }),
    )
    .required(),
});

export const ElementSetListSchema = yup.array().of(ElementSetSchema);

export const UserElementSetsSchema = yup.object().shape({
  sets: ElementSetListSchema.required(),
  elements: ElementListSchema.required(),
  tags: ElementTagListSchema.required(),
});
