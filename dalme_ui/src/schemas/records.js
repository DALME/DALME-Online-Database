import camelcaseKeys from "camelcase-keys";
import { isNil } from "ramda";
import * as yup from "yup";

import { agentsNormalizeInputSchema } from "@/components/forms/agents-field/normalize";
import { foliosNormalizeInputSchema } from "@/components/forms/folios-field/normalize";
import {
  agentsFieldSchema,
  attributesFieldSchema,
  creditsFieldSchema,
  foliosFieldSchema,
} from "@/schemas";

export const recordFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  shortName: yup.string().nullable().required().label("Short name"),
  hasInventory: yup
    .object()
    .shape({
      value: yup
        .boolean()
        .nullable()
        .required()
        .transform((option) => (isNil(option) ? null : Boolean(option.value))),
    })
    .nullable()
    .required()
    .label("List"),
  parent: yup
    .object()
    .shape({ value: yup.string().uuid().nullable() })
    .nullable()
    .label("Parent"),
  sets: yup
    .array()
    .of(yup.object().shape({ value: yup.string().uuid().nullable() }))
    .nullable()
    .label("Sets"),
  attributes: yup.array().of(attributesFieldSchema).label("Attributes"),
  agents: yup
    .array()
    .of(agentsFieldSchema)
    .default(null)
    .nullable()
    .label("Agents"),
  pages: yup
    .array()
    .of(foliosFieldSchema)
    .default(null)
    .nullable()
    .label("Folios"),
  credits: yup
    .array()
    .of(creditsFieldSchema)
    .default(null)
    .nullable()
    .label("Credits"),
};

// Edit object schema
// Transforms API data to the correct shape expected by the form.
export const recordEditSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    shortName: yup.string().required(),
    hasInventory: yup.object().shape({
      value: yup.boolean().required(),
      label: yup.string().required(),
    }),
    parent: yup
      .object()
      .shape({
        value: yup.string().uuid().required(),
        label: yup.string().required(),
      })
      .nullable(),
    sets: yup.array().of(
      yup.object().shape({
        value: yup.string().uuid().required(),
        label: yup.string().required(),
      }),
    ),
    // Just minimal validation here for the attributes. We will apply the
    // full transform elsewhere, as it's very complex.
    attributes: yup.mixed(),
    agents: agentsNormalizeInputSchema,
    pages: foliosNormalizeInputSchema,
    // credits
  })
  .camelCase()
  .transform((data) => ({
    ...data,
    hasInventory: {
      value: data.hasInventory,
      label: data.hasInventory ? "True" : "False",
    },
    parent: {
      value: data.parent.id,
      label: data.parent.name,
    },
    sets: data.sets.map((item) => ({ value: item.id, label: item.name })),
    // TODO: Remove ALL camelcase hackage when we sort out the API renderer.
    // Camelize here because we run a function to normalize the attributes, not
    // a schema like the others (which is why they are omitted here.)
    attributes: camelcaseKeys(data.attributes),
  }));

// POST data schemas.
// Normalizes form data for output to the API.
// folios -> pages
export const recordPostSchema = yup.object().shape({});

export const recordPutSchema = recordPostSchema.shape({
  id: yup.string().uuid().required(),
});
