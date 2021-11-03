import * as yup from "yup";

export const agentListSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.string().uuid().required(),
      standardName: yup.string().required(),
      type: yup
        .object()
        .shape({
          id: yup.number().required(),
          name: yup.string().required(),
        })
        .required(),
      user: yup.string().default(null).nullable(),
    })
    .camelCase(),
);
