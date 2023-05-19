import * as yup from "yup";

export const authSchema = yup
  .object()
  .shape({
    access: yup.string().required(),
    refresh: yup.string(),
    user: yup
      .object()
      .shape({
        id: yup.number().required(),
        username: yup.string().required(),
        email: yup.string().email().required(),
        fullName: yup.string().required(),
        isAdmin: yup.boolean().required(),
        avatar: yup.string().required(),
      })
      .camelCase(),
  })
  .camelCase();
