import * as yup from "yup";
import { transcriptionsFieldSchema } from "@/schemas";

export const pageFieldSchema = yup.object().shape({
  folio: yup.string().nullable().required(),
  damId: yup.object().shape({ value: yup.number().required() }).nullable().required(),
});

export const pageValidators = {
  folio: yup.string().nullable().required().label("Folio"),
  damId: yup
    .object()
    .shape({ value: yup.number().required().label("DAM ID") })
    .nullable()
    .required()
    .label("DAM ID"),
};

export const pageSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  order: yup.number().nullable().required(),
  damId: yup.number().nullable().required(),
  thumbnail_url: yup.string().url().nullable(),
  manifest_url: yup.string().url().nullable(),
  hasImage: yup.boolean().required(),
  hasTranscription: yup.boolean().required(),
  transcription: transcriptionsFieldSchema.nullable(),
});
