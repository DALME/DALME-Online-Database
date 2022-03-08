import { isNil } from "ramda";
import * as yup from "yup";

export const agentListSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.string().uuid().required(),
      standardName: yup.string().required(),
      type: yup
        .object()
        .shape({
          id: yup.number().required(),
          name: yup.string().required(),
        })
        .required(),
      user: yup.string().default(null).nullable(),
    })
    .camelCase(),
);

const creditAgentOptionSchema = yup
  .object()
  .shape({
    value: yup.string().uuid().required(),
    label: yup.string().required(),
    caption: yup.string().uuid().required(),
  })
  .transform((option) => ({
    value: option.id,
    label: option.standard_name,
    caption: option.id,
  }));

export const creditAgentOptionsSchema = yup.array().of(creditAgentOptionSchema);

const creditRoleOptionSchema = yup
  .object()
  .shape({
    value: yup.number().required(),
    label: yup.string().required(),
  })
  .transform((option) => ({
    value: option.id,
    label: option.name,
  }));

export const creditRoleOptionsSchema = yup.array().of(creditRoleOptionSchema);

export const creditOptionSchema = yup.object().shape({
  agent: yup
    .object()
    .shape({ value: yup.string().uuid().required() })
    .required(),
  role: yup.object().shape({ value: yup.number().required() }).required(),
  note: yup
    .string()
    .nullable()
    .test(
      "length",
      "Note cannot be longer than 255 characters",
      (val) => val.length < 256,
    ),
});

export const creditValidators = {
  agent: yup
    .object()
    .shape({ id: yup.string().uuid().required().label("Agent") })
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : { id: option.value }))
    .label("Agent"),
  role: yup
    .object()
    .shape({ id: yup.number().required().label("Role") })
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : { id: option.value }))
    .label("Role"),
  // NOTE: We use the inbuilt quasar validation at the field level for this so
  // no need to defined it with yup. We'll leave it here for clarity.
  note: null,
};
