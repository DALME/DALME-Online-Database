import { isNil } from "ramda";
import * as yup from "yup";

export const apiOptionSchema = yup
  .object()
  .shape({
    id: yup.mixed().required(),
    label: yup.string().required(),
  })
  .transform((option) =>
    isNil(option) ? null : { label: option.label, id: option.value },
  );

export const optionsSchema = yup.array().of(
  yup.object().shape({
    label: yup.string().required(),
    value: yup.string().required(),
  }),
);

export const ownerSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    username: yup.string().required(),
    // TODO: Should be required, disabled for now.
    fullName: yup.string().nullable(),
  })
  .camelCase();
