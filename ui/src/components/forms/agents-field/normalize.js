import { isEmpty } from "ramda";
import * as yup from "yup";

export const empty = () => ({
  agent: null,
  legalPersona: null,
  type: "person",
});

export const agentsNormalizeInputSchema = yup.array().of(
  yup
    .object()
    .shape({
      agent: yup
        .object()
        .shape({
          value: yup.string().uuid().required(),
          label: yup.string().required(),
        })
        .nullable()
        .required()
        .label("Agent"),
      legalPersona: yup
        .object()
        .shape({
          value: yup.string().required(),
          label: yup.string().required(),
        })
        .nullable()
        .required()
        .label("Legal persona"),
      type: yup
        .object()
        .shape({
          value: yup.string().required(),
          label: yup.string().required(),
        })
        .nullable()
        .required()
        .label("Type"),
    })
    .camelCase()
    .transform((data) => ({
      agent: { value: data.id, label: data.name },
      legalPersona: { value: data.legalPersona, label: data.legalPersona },
      type: { value: data.type, label: data.type },
    })),
);

export const normalizeOutputSchema = yup
  .array()
  .nullable()
  .compact((value) => value === empty())
  .of(
    yup
      .object()
      .shape({
        agent: yup.string().uuid().required(),
        legalPersona: yup.string().required(),
        type: yup.string().required(),
      })
      .transform((data) => ({
        agent: data.agent.value,
        legalPersona: data.legalPersona.value,
        type: data.type.value,
      })),
  )
  .transform((final) => (isEmpty(final) ? null : final));
