import * as yup from "yup";

export const groupSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
  description: yup.string().required(),
  properties: yup.object().shape({
    type: yup.number().required(),
    description: yup.string().required(),
  }),
});

export const groupListSchema = yup.array().of(groupSchema);
