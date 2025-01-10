import * as yup from "yup";
import { OptionListSchema } from "@/schemas";

export const TeiElementAttributeSchema = yup.object().shape({
  label: yup.string().required(),
  value: yup.string().required(),
  kind: yup.string().nullable(),
  description: yup.string().nullable(),
  required: yup.boolean().required(),
  editable: yup.boolean().required(),
  default: yup.string().nullable(),
  options: OptionListSchema.nullable(),
});

export const TeiElementAttributeListSchema = yup.array().of(TeiElementAttributeSchema);

export const TeiElementSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  label: yup.string().required(),
  kind: yup.string().required(),
  section: yup.string().required(),
  description: yup.string().required(),
  kbReference: yup.string().required(),
  tag: yup.string().required(),
  compound: yup.boolean().required(),
  placeholder: yup.string().nullable(),
  icon: yup.string().required(),
  attributes: TeiElementAttributeListSchema,
});

export const TeiElementListSchema = yup.array().of(TeiElementSchema);

export const TeiElementSetSchema = yup.object().shape({
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

export const TeiElementSetListSchema = yup.array().of(TeiElementSetSchema);

export const TeiUserElementSetsSchema = yup.object().shape({
  sets: TeiElementSetListSchema.required(),
  elements: TeiElementListSchema.required(),
});
