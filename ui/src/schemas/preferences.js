import * as yup from "yup";

export const preferenceSchema = yup.object().shape({
  general: yup.object().required(),
  sourceEditor: yup.object().default({}),
  lists: yup.object().default({}),
});
