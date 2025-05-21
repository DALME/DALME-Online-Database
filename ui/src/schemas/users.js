import { isNil } from "ramda";
import * as yup from "yup";

import { timeStampSchema } from "@/schemas";

export const userSchema = yup.object().shape({
  avatar: yup.string().default(null).nullable(),
  dateJoined: timeStampSchema.optional(),
  email: yup.string().email().optional(),
  firstName: yup.string().required(),
  fullName: yup.string().nullable(),
  groupIds: yup
    .array()
    .optional()
    .transform((value) => (isNil(value) ? [] : value)),
  id: yup.number().required(),
  isActive: yup.boolean().optional(),
  isStaff: yup.boolean().optional(),
  isSuperuser: yup.boolean().optional(),
  lastLogin: timeStampSchema.optional().default(null).nullable(),
  lastName: yup.string().required(),
  username: yup.string().required(),
});

export const userListSchema = yup.array().of(userSchema);

export const userAttributeSchema = yup.object().shape({
  avatar: yup.string().default(null).nullable(),
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
