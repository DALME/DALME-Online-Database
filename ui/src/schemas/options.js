import * as yup from "yup";

export const optionSchema = yup.object().shape({
  label: yup.string().required(),
  value: yup.mixed().required(),
  description: yup.string(),
  group: yup.string(),
});

export const optionListSchema = yup.array().of(optionSchema);
