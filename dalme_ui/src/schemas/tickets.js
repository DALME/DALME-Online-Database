import * as yup from "yup";

const ticketListDataSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    subject: yup.string().required(),
    commentCount: yup
      .number()
      .nullable()
      .transform((value) => (value === 0 ? null : value)),
    tag: yup
      .string()
      .transform((_, originalValue) =>
        originalValue[0].tag !== "0" ? originalValue[0].tag.trim() : "",
      ),
    file: yup.string().uuid().nullable(),
  })
  .transformKeys((key) => (key === "tags" ? "tag" : key))
  .camelCase();

const ticketListSchema = yup.object().shape({
  count: yup.number().required(),
  next: yup.string().nullable(),
  previous: yup.string().nullable(),
  results: yup.array().of(ticketListDataSchema),
});

export { ticketListSchema };
