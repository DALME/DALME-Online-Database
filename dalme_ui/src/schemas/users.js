import moment from "moment";
import * as yup from "yup";

export const userOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().email().required(),
    })
    .transform((value) => ({
      // TODO: Only necessary cause I don't have a user.profile.
      label: value.full_name || `${value.first_name} ${value.last_name}`,
      value: value.id,
      caption: value.email,
    })),
);

export const userSelectSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.string().required(),
      username: yup.string().required(),
      fullName: yup.string().required(),
    })
    .transform((value) => ({
      id: value.id,
      username: value.username,
      fullName: value.full_name || `${value.first_name} ${value.last_name}`,
    })),
);

export const groupSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
  description: yup.string().required(),
});

export const userSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    username: yup.string().required(),
    fullName: yup.string().nullable(),
    firstName: yup.string().required(),
    lastName: yup.string().required(),
    email: yup.string().email().required(),
    isStaff: yup.boolean().required(),
    isSuperuser: yup.boolean().required(),
    isActive: yup.boolean().required(),
    dateJoined: yup
      .string()
      .required()
      .transform((value) =>
        moment(new Date(value)).format("DD-MMM-YYYY HH:mm"),
      ),
    lastLogin: yup
      .string()
      .required()
      .transform((value) =>
        moment(new Date(value)).format("DD-MMM-YYYY HH:mm"),
      ),
    groups: yup.array().of(groupSchema).default(null).nullable(),
    profile: yup
      .object()
      .shape({
        fullName: yup.string().required(),
        primaryGroup: yup
          .object()
          .shape({
            id: yup.number().required(),
            name: yup.string().required(),
            description: yup.string().required(),
          })
          .default(null)
          .nullable(),
      })
      .default(null)
      .nullable()
      .camelCase(),
    avatar: yup.string().default(null).nullable(),
  })
  .camelCase();

export const userListSchema = yup.array().of(userSchema);

// export const userListSchema = yup.array().of(
//   yup
//     .object()
//     .shape({
//       id: yup.number().required(),
//       username: yup.string().required(),
//       // TODO: Should be required but I don't have a profile.
//       fullName: yup.string().nullable(),
//       email: yup.string().required(),
//       lastLogin: yup
//         .string()
//         .required()
//         .transform((value) =>
//           moment(new Date(value)).format("DD-MMM-YYYY HH:mm"),
//         ),
//       isActive: yup.boolean().required(),
//       isStaff: yup.boolean().required(),
//       avatar: yup.string().default(null).nullable(),
//     })
//     .camelCase(),
// );
