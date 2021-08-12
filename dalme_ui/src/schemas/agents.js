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
          objId: yup.number().required(),
          name: yup.string().required(),
        })
        .transformKeys((value) => (value === "id" ? "objId" : value))
        .required(),
      user: yup.string().default(null).nullable(),
    })
    .camelCase(),
);
