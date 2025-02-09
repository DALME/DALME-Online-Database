import * as yup from "yup";

export const languageSchema = yup
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
  .camelCase();

export const languageListSchema = yup.array().of(languageSchema);

export const completionSchema = yup
  .object()
  .shape({
    label: yup.string().required(),
    type: yup.string().nullable(),
    info: yup.mixed().nullable(),
    apply: yup.mixed().nullable(),
    detail: yup.mixed().nullable(),
  })
  .camelCase();

export const completionListSchema = yup.array().of(completionSchema);
