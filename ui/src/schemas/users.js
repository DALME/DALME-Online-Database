import { isNil } from "ramda";
import * as yup from "yup";

import { timeStampSchema } from "@/schemas";

export const userSchema = yup.object().shape({
  // groups: yup.array().of(groupSchema).default(null).nullable(),
  avatar: yup.string().default(null).nullable(),
  dateJoined: timeStampSchema.required(),
  email: yup.string().email().required(),
  firstName: yup.string().required(),
  fullName: yup.string().nullable(),
  groupIds: yup
    .array()
    .required()
    .transform((value) => (isNil(value) ? [] : value)),
  id: yup.number().required(),
  isActive: yup.boolean().required(),
  isStaff: yup.boolean().required(),
  isSuperuser: yup.boolean().required(),
  lastLogin: timeStampSchema.default(null).nullable(),
  lastName: yup.string().required(),
  username: yup.string().required(),
});

export const userListSchema = yup.array().of(userSchema);

export const userAttributeSchema = yup.object().shape({
  avatar: yup.string().default(null).nullable(),
  email: yup.string().email().required(),
  fullName: yup.string().required(),
  id: yup.number().required(),
  username: yup.string().required(),
});

export const usersAsOptionsSchema = yup.array().of(
  yup.object().shape({
    caption: yup.string().required(),
    label: yup.string().required(),
    value: yup.string().required(),
  }),
);
