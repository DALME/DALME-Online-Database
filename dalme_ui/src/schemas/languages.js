import * as yup from "yup";

export const languageOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().default(null).nullable(),
    })
    .transform((value) => ({
      label: value.name,
      value: value.id,
      caption: value.glottocode,
    })),
);

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
        .length(3)
        .default(null)
        .nullable()
        .transform((val) => (!val ? null : val)), // Null out empty strings.
      glottocode: yup.string().required(),
    })
    .camelCase(),
);
