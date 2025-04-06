import * as yup from "yup";

export const agentSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    agentType: yup
      .string()
      .matches(/(Person|Organization)/, { excludeEmptyString: true })
      .required(),
    user: yup.string().default(null).nullable(),
  })
  .camelCase();

export const agentListSchema = yup.array().of(agentSchema);

const agentOptionSchema = yup
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

export const agentOptionsSchema = yup.array().of(agentOptionSchema);

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

const legalPersonaOptionSchema = yup.object().shape({
  value: yup.string().required(),
  label: yup
    .string()
    .required()
    .transform((value) => value.charAt(0).toUpperCase() + value.slice(1)),
});

export const legalPersonaOptionsSchema = yup.array().of(legalPersonaOptionSchema);

export const creditsFieldSchema = yup.object().shape({
  agent: yup.object().shape({ value: yup.string().uuid().required() }).nullable(),
  role: yup.object().shape({ value: yup.number().required() }).nullable(),
  note: yup
    .string()
    .nullable()
    .test("length", "Note cannot be longer than 255 characters", (val) => val.length < 256),
});

export const agentsFieldSchema = yup.object().shape({
  agent: yup.object().shape({ value: yup.string().uuid().required() }).nullable(),
  legalPersona: yup.object().shape({ value: yup.string().required() }).nullable(),
});

export const agentValidators = {
  agent: yup
    .object()
    .shape({ value: yup.string().required().label("Agent") })
    .nullable()
    .required()
    .label("Agent"),
  legalPersona: yup
    .object()
    .shape({ value: yup.string().required().label("Legal persona") })
    .nullable()
    .required()
    .label("Legal persona"),
};

export const creditValidators = {
  agent: yup
    .object()
    .shape({ value: yup.string().required().label("Agent") })
    .nullable()
    .required()
    .label("Agent"),
  role: yup
    .object()
    .shape({ value: yup.number().required().label("Role") })
    .nullable()
    .required()
    .label("Role"),
  // NOTE: We use the inbuilt quasar validation at the field level for this so
  // no need to defined it with yup. We'll leave it here for clarity.
  note: null,
};
