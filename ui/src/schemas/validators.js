import * as yup from "yup";

import { attributeValidators } from "./attributes";

export const validators = {
  ...attributeValidators,
  name: yup.object().nullable().required(),
};
