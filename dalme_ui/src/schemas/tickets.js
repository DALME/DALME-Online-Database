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
    description: yup.string().default(null).nullable(),
    tags: yup
      .string()
      .transform((_, originalValue) =>
        head(originalValue).tag !== "0" ? head(originalValue).tag.trim() : "",
      ),
    file: attachmentSchema.default(null).nullable(),
    commentCount: yup
      .number()
      .default(null)
      .nullable()
      .transform((value) => (value === 0 ? null : value)),
    creationUser: yup
      .object()
      .shape({
        id: yup.number().required(),
        username: yup.string().required(),
        fullName: yup.string().required(),
        avatar: yup.string().url().default(null).nullable(),
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
    description: yup.string().default(null).nullable(),
    tags: yup
      .string()
      .transform((_, originalValue) =>
        head(originalValue).tag !== "0" ? head(originalValue).tag.trim() : "",
      ),
    file: yup.string().default(null).nullable(),
    commentCount: yup
      .number()
      .default(null)
      .nullable()
      .transform((value) => (value === 0 ? null : value)),
    creationUser: yup
      .object()
      .shape({
        id: yup.number().required(),
        username: yup.string().required(),
        fullName: yup.string().required(),
        avatar: yup.string().url().default(null).nullable(),
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
  next: yup.string().default(null).nullable(),
  previous: yup.string().default(null).nullable(),
  results: yup.array().of(ticketSchema),
});
