import * as yup from "yup";

export const sessionSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    username: yup.string().required(),
  })
  .camelCase();
