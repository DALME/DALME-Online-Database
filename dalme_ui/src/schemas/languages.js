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
      iso6393: yup.string().length(3).default(null).nullable(),
      glottocode: yup.string().required(),
    })
    .camelCase(),
);
