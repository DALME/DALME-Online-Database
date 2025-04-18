import * as yup from "yup";

import { attachmentSchema, userAttributeSchema } from "@/schemas";

export const ticketSchema = yup
  .object()
  .shape({
    assignedTo: userAttributeSchema.default(null).nullable(),
    closingDate: yup.string().default(null).nullable(),
    closingUser: userAttributeSchema.default(null).nullable(),
    commentCount: yup.number().default(0).nullable(),
    creationTimestamp: yup.string(),
    creationUser: userAttributeSchema.required(),
    description: yup
      .string()
      .default(null)
      .nullable()
      .transform((_, value) => {
        return value === null ? "" : String(value);
      }),
    id: yup.string().uuid().required(),
    modificationTimestamp: yup.string(),
    modificationUser: userAttributeSchema.required(),
    number: yup.number().required(),
    status: yup.boolean().required(),
    subject: yup.string().required(),
    tags: yup.array().of(
      yup
        .object()
        .shape({
          tag: yup
            .string()
            // necessary to deal with malformed tags
            .nullable()
            .transform((value) => (value === "0" ? null : value)),
        })
        .camelCase(),
    ),
    files: yup.array().of(attachmentSchema),
    url: yup.string().url().default(null).nullable(),
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
    id: yup.string().uuid().required(),
    number: yup.number().required(),
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
  id: yup.string().uuid().required(),
});

export const ticketSubmitSchemas = {
  create: ticketPostSchema,
  update: ticketPutSchema,
};
