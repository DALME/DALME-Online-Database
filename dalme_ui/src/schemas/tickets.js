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
    tags: yup.array().of(
      yup
        .object()
        .shape({
          tag: yup.string().required(),
          tagTypeName: yup.string().required(),
        })
        .camelCase(),
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

export const ticketListSchema = yup.array().of(ticketSchema);

export const ticketFieldValidation = {
  subject: yup.string().nullable().required().label("Subject"),
  description: yup.string().nullable().required().label("Description"),
  status: yup
    .object()
    .shape({
      value: yup.number().min(0).max(1).nullable().required().label("Status"),
    })
    .nullable()
    .required()
    .label("Status"),
  assignedTo: yup
    .object()
    .shape({
      value: yup.number().nullable().label("Assigned to"),
    })
    .nullable()
    .label("Assigned to"),
  tags: yup.array().of(
    yup
      .object()
      .shape({
        value: yup.string().required(),
      })
      .nullable()
      .label("Tags"),
  ),
  // TODO: url
  // TODO: file
};

export const ticketEditSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    subject: yup.string().required(),
    description: yup.string().required(),
    status: yup.object().shape({
      value: yup.number().min(0).max(1).required(),
      label: yup.string().required(),
    }),
    assignedTo: yup.object().shape({
      value: yup.number().required(),
      label: yup.string().required(),
    }),
    tags: yup.array().of(
      yup.object().shape({
        value: yup.string().required(),
        label: yup.string().required(),
      }),
    ),
    // TODO: url
    // TODO: file
  })
  .camelCase()
  .transform((data) => data);

export const ticketStatusOptionsSchema = yup.array().of(
  yup.object().shape({
    value: yup.number().required(),
    label: yup.string().required(),
  }),
);

export const ticketTagOptionsSchema = yup.array().of(
  yup.object().shape({
    value: yup.string().required(),
    label: yup.string().required(),
  }),
);

// POST/PUT data schemas.
// Normalizes ticket form data for output to the API.
const ticketPostSchema = yup.object().shape({
  subject: yup.string().required(),
  description: yup.string().required(),
  status: yup.number().default(null).nullable(),
  assignedTo: yup.number().default(null).nullable(),
  // TODO: tags are array or...?
  // TODO: url
  // TODO: file
});

const ticketPutSchema = ticketPostSchema.shape({
  id: yup.number().required(),
});

export const ticketSubmitSchemas = {
  create: ticketPostSchema,
  update: ticketPutSchema,
};
