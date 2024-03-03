import * as yup from "yup";

export const imageOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.number().required(),
      value: yup.number().required(),
      caption: yup.string().required(),
    })
    .transform((value) => ({
      label: value.dam_id,
      value: value.dam_id,
      caption: value.title,
    })),
);
