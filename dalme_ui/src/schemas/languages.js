import * as yup from "yup";

export const languageListSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.number().required(),
      name: yup.string().required(),
      type: yup
        .object()
        .shape({
          id: yup.number().required(),
          name: yup.string().required(),
        })
        .required(),
      parent: yup
        .object()
        .shape({
          id: yup.number().required(),
          name: yup.string().required(),
        })
        .default(null)
        .nullable(),
      iso6393: yup
        .string()
        .default(null)
        .nullable()
        .transform((val) => (!val ? null : val)), // Null out empty strings.
      glottocode: yup.string().required(),
    })
    .camelCase(),
);
