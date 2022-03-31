import camelcaseKeys from "camelcase-keys";
import { isNil } from "ramda";
import * as yup from "yup";

import {
  agentsFieldSchema,
  attributesFieldSchema,
  foliosFieldSchema,
  creditsFieldSchema,
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
  agents: yup.array().of(agentsFieldSchema).label("Agents"),
  folios: yup.array().of(foliosFieldSchema).label("Folios"),
  credits: yup.array().of(creditsFieldSchema).label("Credits"),
};

// Edit existing object schema.
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
    // agents
    // folios (how do we do folios vs pages elsewhere, i've forgotten).
    // TODO: Needs to be ordered by order and normalize the actual order field
    // if it's nonsensical.
    // "pages": [
    //     {
    //         "id": "2af6be21-1510-42d1-beaf-a5de9f4f391c",
    //         "name": "4v",
    //         "dam_id": 5342,
    //         "order": 10,
    //         "has_image": true,
    //         "has_transcription": true
    //     },
    // ],
    // credits
  })
  .camelCase()
  .transform((validated) => ({
    ...validated,
    hasInventory: {
      value: validated.hasInventory,
      label: validated.hasInventory ? "True" : "False",
    },
    parent: {
      value: validated.parent.id,
      label: validated.parent.name,
    },
    sets: validated.sets.map((item) => ({ value: item.id, label: item.name })),
    // TODO: Remove ALL camelcase hackakge when we sort out the API renderer.
    // We can't do this in the schema proper as the object shape is dynamic.
    attributes: camelcaseKeys(validated.attributes),
    // agents: normalizeAgentsInput(validated.agents),
    // credits: normalizeCreditsInput(validated.credits),
  }));

// POST data schemas.
// Normalizes form data for output to the API.
export const recordPostSchema = yup.object().shape({});

export const recordPutSchema = recordPostSchema.shape({
  id: yup.string().uuid().required(),
});
