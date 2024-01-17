import * as yup from "yup";

export const tenantSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
});
