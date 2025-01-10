import * as yup from "yup";

export const OptionSchema = yup.object().shape({
  label: yup.string().required(),
  value: yup.string().required(),
  description: yup.string(),
  group: yup.string(),
});

export const OptionListSchema = yup.array().of(OptionSchema);
