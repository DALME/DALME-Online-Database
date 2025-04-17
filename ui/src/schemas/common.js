import * as yup from "yup";

export const attachmentSchema = yup.object().shape({
  filename: yup.string().required(),
  source: yup.string().required(),
  filetype: yup.string().required(),
});

export const optionsSchema = yup.array().of(
  yup.object().shape({
    label: yup.string().required(),
    value: yup.string().required(),
    group: yup.string(),
    caption: yup.string(),
  }),
);

export const baseContentTypeSchema = yup.object().shape({
  id: yup.number().required(),
  appLabel: yup.string().required(),
  model: yup.string().required(),
});

export const timeStampSchema = yup.date().default(null).nullable();

const singleDateSchema = yup.object().shape({
  date: yup
    .date()
    .transform((value) => (value == null ? null : new Date(value)))
    .nullable(),
  day: yup.number().nullable(),
  era: yup.string().nullable(),
  isRange: yup.boolean().default(false),
  month: yup.number().nullable(),
  text: yup.string().required(),
  year: yup.number().nullable(),
});

const dateRangeSchema = yup.object().shape({
  end: singleDateSchema.required(),
  isRange: yup.boolean().default(true),
  start: singleDateSchema.required(),
  text: yup.string().required(),
});

export const dateSchema = yup.lazy((value) =>
  value?.isRange ? dateRangeSchema.nullable() : singleDateSchema.nullable(),
);

export const editionSchema = yup.object().shape({
  name: yup.string().required(),
  type: yup.string().required(),
  zoteroKey: yup.string().required(),
});

export const registerSchema = yup.object().shape({
  format: yup.object().shape({
    format: yup.string().required(),
    label: yup.string().required(),
    support: yup.string().required(),
  }),
  loc: yup.string().required(),
  name: yup.string().required(),
  type: yup.string().required(),
  url: yup.string().url().nullable(),
});
