import moment from "moment";
import { head } from "ramda";
import * as yup from "yup";

export const attachmentSchema = yup.object().shape({
  filename: yup.string().required(),
  source: yup.string().required(),
  type: yup.string().required(),
});

export const ticketDetailSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    status: yup.boolean().required(),
    subject: yup.string().required(),
    description: yup.string().nullable(),
    tags: yup
      .string()
      .transform((_, originalValue) =>
        head(originalValue).tag !== "0" ? head(originalValue).tag.trim() : "",
      ),
    file: attachmentSchema,
    commentCount: yup
      .number()
      .nullable()
      .transform((value) => (value === 0 ? null : value)),
    creationUser: yup
      .object()
      .shape({
        id: yup.number().required(),
        username: yup.string().required(),
        fullName: yup.string().required(),
        avatar: yup.string().url().nullable(),
      })
      .camelCase(),
    creationTimestamp: yup
      .string()
      .transform((value) => moment(new Date(value)).format("DD-MMM-YYYY")),
    closingDate: yup
      .string()
      .transform((value) => moment(new Date(value)).format("DD-MMM-YYYY")),
  })
  .camelCase();

export const ticketSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    status: yup.boolean().required(),
    subject: yup.string().required(),
    description: yup.string().nullable(),
    tags: yup
      .string()
      .transform((_, originalValue) =>
        head(originalValue).tag !== "0" ? head(originalValue).tag.trim() : "",
      ),
    file: yup.string().nullable(),
    commentCount: yup
      .number()
      .nullable()
      .transform((value) => (value === 0 ? null : value)),
    creationUser: yup
      .object()
      .shape({
        id: yup.number().required(),
        username: yup.string().required(),
        fullName: yup.string().required(),
        avatar: yup.string().url().nullable(),
      })
      .camelCase(),
    creationTimestamp: yup
      .string()
      .transform((value) => moment(new Date(value)).format("DD-MMM-YYYY")),
    closingDate: yup
      .string()
      .transform((value) => moment(new Date(value)).format("DD-MMM-YYYY")),
  })
  .camelCase();

export const ticketListSchema = yup.object().shape({
  count: yup.number().required(),
  next: yup.string().nullable(),
  previous: yup.string().nullable(),
  results: yup.array().of(ticketSchema),
});
