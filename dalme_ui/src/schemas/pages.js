import * as yup from "yup";

export const pageOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().required(),
    })
    .transform((value) => ({
      label: value.id,
      value: value.id,
      caption: `Name: ${value.name}<br> DAM ID: ${
        value.dam_id || "None"
      }<br> Order: ${value.order}`,
    })),
);
