import camelcaseKeys from "camelcase-keys";
import { isNil } from "ramda";
import * as yup from "yup";

import { agentsNormalizeInputSchema } from "@/components/forms/agents-field/normalize";
import { foliosNormalizeInputSchema } from "@/components/forms/folios-field/normalize";
import {
  attributeSchema,
  agentListSchema,
  agentsFieldSchema,
  attributesFieldSchema,
  collectionAttributeSchema,
  creditsFieldSchema,
  pageFieldSchema,
  pageSchema,
  timeStampSchema,
  userAttributeSchema,
  workflowSchema,
  recordGroupAttributeSchema,
  publicationAttributeSchema,
} from "@/schemas";

export const recordSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  shortName: yup.string().required(),
  owner: userAttributeSchema.required(),
  attributes: yup.array().of(attributeSchema).required(),
  noFolios: yup.number().required(),
  isPrivate: yup.boolean().required(),
  commentCount: yup.number().required(),
  creationTimestamp: timeStampSchema.required(),
  creationUser: userAttributeSchema.required(),
  modificationTimestamp: timeStampSchema.required(),
  modificationUser: userAttributeSchema.required(),
  workflow: workflowSchema.nullable(),
});

export const recordListSchema = yup.array().of(recordSchema);

export const recordAttributeSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  shortName: yup.string().required(),
});

export const recordDetailSchema = yup.object().shape({
  agents: agentListSchema,
  attributes: yup.array().of(attributeSchema).required(),
  collections: yup.array().of(collectionAttributeSchema).required(),
  commentCount: yup.number().required(),
  creationTimestamp: timeStampSchema.required(),
  creationUser: userAttributeSchema.required(),
  creditLine: yup.string().required(),
  id: yup.string().uuid().required(),
  isPrivate: yup.boolean().required(),
  modificationTimestamp: timeStampSchema.required(),
  modificationUser: userAttributeSchema.required(),
  name: yup.string().required(),
  noFolios: yup.number().required(),
  noTranscriptions: yup.number().required(),
  owner: userAttributeSchema.required(),
  pages: yup.array().of(pageSchema).nullable(),
  shortName: yup.string().required(),
  parent: yup.lazy((value) =>
    "parent" in value ? recordGroupAttributeSchema : publicationAttributeSchema,
  ),
  workflow: workflowSchema,
});

// Field-level validation rules/schemas.
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
  parent: yup.object().shape({ value: yup.string().uuid().nullable() }).nullable().label("Parent"),
  sets: yup
    .array()
    .of(yup.object().shape({ value: yup.string().uuid().nullable() }))
    .default(null)
    .nullable()
    .label("Sets"),
  attributes: yup.array().of(attributesFieldSchema).required().label("Attributes"),
  agents: yup.array().of(agentsFieldSchema).default(null).nullable().label("Agents"),
  pages: yup.array().of(pageFieldSchema).default(null).nullable().label("Folios"),
  credits: yup.array().of(creditsFieldSchema).default(null).nullable().label("Credits"),
};

// Edit object schema
// Transforms API data to the correct shape expected by the form.
export const recordEditSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    shortName: yup.string().required(),
    // hasInventory: yup.object().shape({
    //   value: yup.boolean().required(),
    //   label: yup.string().required(),
    // }),
    // parent: yup
    //   .object()
    //   .shape({
    //     value: yup.string().uuid().required(),
    //     label: yup.string().required(),
    //   })
    //   .nullable(),
    // sets: yup.array().of(
    //   yup.object().shape({
    //     value: yup.string().uuid().required(),
    //     label: yup.string().required(),
    //   }),
    // ),
    agents: agentsNormalizeInputSchema,
    // NOTE: Just minimal validation here for the attributes. We apply the full
    // transform elsewhere, as it's very complex and better suits a function.
    attributes: yup.mixed(),
    // credits: creditsNormalizeInputSchema,
    pages: foliosNormalizeInputSchema,
  })
  .camelCase()
  .transform((data) => ({
    ...data,
    // hasInventory: {
    //   value: data.hasInventory,
    //   label: data.hasInventory ? "True" : "False",
    // },
    // parent: {
    //   value: data.parent.id,
    //   label: data.parent.name,
    // },
    // sets: data.sets.map((item) => ({ value: item.id, label: item.name })),
    // TODO: Remove ALL camelcase hackage when we sort out the API renderer.
    // Until then, we camelize here because we run a function not a schema to
    // normalize the attributes so we can't call on yup to camelCase the data.
    attributes: camelcaseKeys(data.attributes),
  }));

// TODO: Ported back.
export const recordOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().uuid().required(),
      caption: yup.string().uuid().required(),
    })
    .transform((value) => ({
      label: value.name,
      value: value.id,
      caption: value.id,
    })),
);

// POST/PUT data schemas.
// Normalizes source form data for output to the API.
const recordPostSchema = yup.object().shape({
  name: yup.string().required(),
  shortName: yup.string().required(),
  parent: yup.string().uuid().default(null).nullable(),
  hasInventory: yup.boolean().default(false).required(),
  isPrivate: yup.boolean().default(false).required(),
  primaryDataset: yup.string().uuid().default(null).nullable(),
  // TODO: Make a payload with all these and use that as yer guide.
  // sets,
  // agents,
  // attributes,
  // credits,
  // pages,
});

const recordPutSchema = recordPostSchema.shape({
  id: yup.string().uuid().required(),
});

export const recordSubmitSchemas = {
  create: recordPostSchema,
  update: recordPutSchema,
};
