import * as yup from "yup";

export const ownerSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    username: yup.string().required(),
    fullName: yup.string().required(),
  })
  .camelCase();
