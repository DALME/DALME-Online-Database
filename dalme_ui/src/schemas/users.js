import * as yup from "yup";
import { timeStampSchema, preferenceSchema, groupSchema } from "@/schemas";

export const userSchema = yup.object().shape({
  id: yup.number().required(),
  username: yup.string().required(),
  fullName: yup.string().nullable(),
  firstName: yup.string().required(),
  lastName: yup.string().required(),
  email: yup.string().email().required(),
  isStaff: yup.boolean().required(),
  isSuperuser: yup.boolean().required(),
  isActive: yup.boolean().required(),
  dateJoined: timeStampSchema.required(),
  lastLogin: timeStampSchema.nullable(),
  groups: yup.array().of(groupSchema).default(null).nullable(),
  avatar: yup.string().default(null).nullable(),
  preferences: preferenceSchema.nullable(),
});

export const userListSchema = yup.array().of(userSchema);

export const userAttributeSchema = yup.object().shape({
  id: yup.number().required(),
  username: yup.string().required(),
  fullName: yup.string().required(),
  email: yup.string().email().required(),
  avatar: yup.string().default(null).nullable(),
});

export const usersAsOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().required(),
    })
    .transform((value) => ({
      // TODO: Only necessary because JHHR doesn't have a user.profile.
      label: value.fullName || `${value.firstName} ${value.lastName}`,
      value: value.id,
      caption: value.username,
    })),
);

export const userLoginSchema = yup.object().shape({
  id: yup.number().required(),
  username: yup.string().required(),
  fullName: yup.string().nullable(),
  email: yup.string().email().required(),
  avatar: yup.string().default(null).nullable(),
  isAdmin: yup.boolean().required(),
  preferences: preferenceSchema.nullable(),
  groups: yup.array().required(),
});
