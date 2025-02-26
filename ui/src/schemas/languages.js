import * as yup from "yup";

export const languageSchema = yup
  .object()
  .shape({
    glottocode: yup.string().required(),
    id: yup.number().required(),
    name: yup.string().required(),
    isDialect: yup.boolean().required(),
    iso6393: yup
      .string()
      .length(3)
      .default(null)
      .nullable()
      .transform((val) => (!val ? null : val)), // Null out empty strings.
    parent: yup.lazy(() => languageSchema.default(null).nullable()),
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
