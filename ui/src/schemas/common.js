import * as yup from "yup";
import { DateTime } from "luxon";

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

export const timeStampSchema = yup
  .string()
  .transform((value) => DateTime.fromISO(value).toLocaleString(DateTime.DATETIME_MED));
