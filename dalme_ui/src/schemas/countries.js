import * as yup from "yup";

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
