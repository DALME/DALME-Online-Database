import * as yup from "yup";

export const countryOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().default(null).nullable(),
    })
    .transform((value) => ({
      label: value.nam,
      value: value.id,
    })),
);

export const countryListSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.number().required(),
      name: yup.string().required(),
      alpha2Code: yup.string().required(),
      alpha3Code: yup.string().required(),
      numCode: yup.number().required(),
    })
    .camelCase(),
);
