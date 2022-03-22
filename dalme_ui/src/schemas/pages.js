import * as yup from "yup";

export const folioOptionSchema = yup.object().shape({});

export const foliosFieldSchema = yup.object().shape({
  folio: yup.string().nullable().required(),
  damId: yup
    .object()
    .shape({ value: yup.number().required() })
    .nullable()
    .required(),
});

export const folioValidators = {
  folio: yup.string().nullable().required().label("Folio"),
  damId: yup
    .object()
    .shape({ value: yup.number().required().label("DAM ID") })
    .nullable()
    .required()
    .label("DAM ID"),
};
