import moment from "moment";
import * as yup from "yup";

export const commentPayloadSchema = yup.object().shape({
  body: yup.string().required(),
  model: yup.string().required(),
  object: yup.lazy((val) =>
    typeof val === "number" ? yup.number() : yup.string(),
  ),
});

export const commentSchema = yup
  .object()
  .shape({
    body: yup.string().required(),
    creationUser: yup
      .object()
      .shape({
        id: yup.number().required(),
        username: yup.string().required(),
        // TODO: Should be required but I don't have a profile.
        fullName: yup.string().nullable(),
        avatar: yup.string().url().nullable(),
      })
      .required()
      .camelCase(),
    creationTimestamp: yup
      .string()
      .required()
      .transform((value) =>
        moment(new Date(value)).format("DD-MMM-YYYY HH:mm"),
      ),
  })
  .camelCase();

export const commentsSchema = yup.object().shape({
  data: yup.array().of(commentSchema),
  recordsFiltered: yup.number().required(),
  recordsTotal: yup.number().required(),
});
