import * as yup from "yup";

export const groupOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().required(),
    })
    .transform((value) => ({
      label: value.name,
      value: value.id,
      caption: value.description,
    })),
);