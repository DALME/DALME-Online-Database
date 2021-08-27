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
          objId: yup.number().required(),
          name: yup.string().required(),
        })
        .transformKeys((value) => (value === "id" ? "objId" : value))
        .required(),
      parent: yup
        .object()
        .shape({
          objId: yup.number().required(),
          name: yup.string().required(),
        })
        .transformKeys((value) => (value === "id" ? "objId" : value))
        .default(null)
        .nullable(),
      iso6393: yup.string().default(null).nullable(),
      glottocode: yup.string().required(),
    })
    .camelCase(),
);
