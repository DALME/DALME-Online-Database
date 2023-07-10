import * as yup from "yup";
import { userLoginSchema } from "@/schemas";

export const authSchema = yup
  .object()
  .shape({
    access: yup.string().required(),
    refresh: yup.string(),
    user: userLoginSchema,
  })
  .camelCase();
