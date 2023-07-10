import * as yup from "yup";

import { unpackPseudoAttributes } from "@/components/forms/attributes-field/normalize";
import { userAttributeSchema } from "./common";

export const setOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().nullable(),
    })
    .transform((value) => ({
      label: value.name,
      value: value.id,
      caption: value.detail_string,
    })),
);

const setTypeSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
});

const permissionSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
});

const collectionSetSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    memberCount: yup.number().required(),
    description: yup.string().required(),
    isPublic: yup.boolean().required(),
    hasLanding: yup.boolean().required(),
    owner: userAttributeSchema.required(),
    permissions: permissionSchema.required(),
  })
  .camelCase();

const corporaSetSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    memberCount: yup.number().required(),
    description: yup.string().required(),
    owner: userAttributeSchema.required(),
    permissions: permissionSchema.required(),
  })
  .camelCase();

const datasetSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    memberCount: yup.number().required(),
    description: yup.string().required(),
    owner: userAttributeSchema.required(),
    datasetUsergroup: yup.object().shape({
      id: yup.number().required(),
      name: yup.string().required(),
    }),
  })
  .camelCase();

const worksetSchema = yup
  .object()
  .shape({
    creationTimestamp: yup.string().required(),
    datasetUsergroup: yup.string().default(null).nullable(),
    description: yup.string().required(),
    detailString: yup.string().required(),
    endpoint: yup.string().required(),
    hasLanding: yup.boolean().default(null).nullable(),
    id: yup.string().uuid().required(),
    isPublic: yup.boolean().default(null).nullable(),
    memberCount: yup.number().required(),
    name: yup.string().required(),
    owner: userAttributeSchema.required(),
    permissions: permissionSchema.required(),
    worksetProgress: yup.number().required(),
    publicMemberCount: yup.number().required(),
    setType: setTypeSchema.required(),
  })
  .camelCase();

export const setMembersSchema = yup.object().shape({
  count: yup.number().required(),
  data: yup.array().of(
    yup
      .object()
      .shape({
        id: yup.string().uuid().required(),
        name: yup.string().required(),
        isPublic: yup.boolean().required(),
      })
      .camelCase(),
  ),
});

export const setDetailSchema = yup
  .object()
  .shape({
    // TODO: Break out into setAttributesSchema. Do same for source.
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    setType: setTypeSchema.required(),
    isPublic: yup.boolean().default(null).nullable(),
    hasLanding: yup.boolean().default(null).nullable(),
    endpoint: yup.string().default(null).nullable(),
    owner: userAttributeSchema.required(),
    permissions: permissionSchema.required(),
    description: yup.string().required(),
    worksetProgress: yup.number().default(null).nullable(),
    statTitle: yup.string().default(null).nullable(),
    statText: yup.string().default(null).nullable(),
    memberCount: yup.number().required(),
    publicMemberCount: yup.number().required(),
  })
  .camelCase();

export const setListSchema = (setType) => {
  const setMap = {
    corpora: corporaSetSchema,
    collections: collectionSetSchema,
    datasets: datasetSchema,
    worksets: worksetSchema,
  };
  return yup.array().of(setMap[setType]);
};

// POST/PUT data schemas.
// Normalizes set form data for output to the API.
const setPostSchema = yup
  .object()
  .shape({
    name: yup.string().required(),
    description: yup.string().required(),
    isPublic: yup.boolean().default(null).nullable(),
    hasLanding: yup.boolean().default(null).nullable(),
    statTitle: yup.string().default(null).nullable(),
    statText: yup.string().default(null).nullable(),
  })
  .transform((data) => ({
    ...data,
    ...unpackPseudoAttributes(data),
  }));

const setPutSchema = setPostSchema.shape({
  id: yup.string().uuid().required(),
});

export const setSubmitSchemas = {
  create: setPostSchema,
  update: setPutSchema,
};
