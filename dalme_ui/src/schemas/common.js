import * as yup from "yup";

export const optionsSchema = yup.array().of(
  yup.object().shape({
    label: yup.string().required(),
    value: yup.string().required(),
  }),
);

export const ownerSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    username: yup.string().required(),
    fullName: yup.string().required(),
  })
  .camelCase();
