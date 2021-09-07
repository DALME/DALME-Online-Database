import * as yup from "yup";

import { ownerSchema } from "./common";

const setTypeSchema = yup
  .object()
  .shape({
    objId: yup.number().required(),
    name: yup.string().required(),
  })
  .transformKeys((value) => (value === "id" ? "objId" : value));

const permissionSchema = yup
  .object()
  .shape({
    objId: yup.number().required(),
    name: yup.string().required(),
  })
  .transformKeys((value) => (value === "id" ? "objId" : value));

const collectionSetSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    memberCount: yup.number().required(),
    description: yup.string().required(),
    isPublic: yup.boolean().required(),
    hasLanding: yup.boolean().required(),
    owner: ownerSchema.required(),
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
    owner: ownerSchema.required(),
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
    owner: ownerSchema.required(),
    datasetUsergroup: yup
      .object()
      .shape({
        objId: yup.number().required(),
        name: yup.string().required(),
      })
      .transformKeys((value) => (value === "id" ? "objId" : value)),
  })
  .camelCase();

const worksetSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    memberCount: yup.number().required(),
    description: yup.string().required(),
    endpoint: yup.string().required(),
    owner: ownerSchema.required(),
    permissions: permissionSchema.required(),
  })
  .camelCase();

export const setMembersSchema = yup.object().shape({
  count: yup.number().required(),
  data: yup.array().of(
    yup
      .object()
      .shape({
        objId: yup.string().uuid().required(),
        name: yup.string().required(),
        isPublic: yup.boolean().required(),
      })
      .transformKeys((value) => (value === "id" ? "objId" : value))
      .camelCase(),
  ),
});

export const setDetailSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    setType: setTypeSchema.required(),
    isPublic: yup.boolean().default(null).nullable(),
    hasLanding: yup.boolean().default(null).nullable(),
    endpoint: yup.string().default(null).nullable(),
    owner: ownerSchema.required(),
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
