import * as yup from "yup";

import {
  agentSchema,
  attributeSchema,
  baseContentTypeSchema,
  recordAttributeSchema,
  timeStampSchema,
  userAttributeSchema,
} from "@/schemas";

const baseRecordGroupSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  shortName: yup.string().required(),
  owner: userAttributeSchema.required(),
  parent: agentSchema.required(),
  parentType: baseContentTypeSchema.required(),
  children: yup.array().of(recordAttributeSchema).required(),
  attributes: yup.array().of(attributeSchema).required(),
  isPrivate: yup.boolean().required(),
  noRecords: yup.number().required(),
  commentCount: yup.number().required(),
  creationTimestamp: timeStampSchema.required(),
  creationUser: userAttributeSchema.required(),
  modificationTimestamp: timeStampSchema.required(),
  modificationUser: userAttributeSchema.required(),
  type: yup.string().optional(),
});

export const recordGroupSchema = baseRecordGroupSchema.omit(["type"]);

export const recordGroupListSchema = yup.array().of(recordGroupSchema);

export const recordGroupAttributeSchema = baseRecordGroupSchema.omit(["children"]);
