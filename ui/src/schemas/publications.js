import * as yup from "yup";
import {
  attributeSchema,
  recordAttributeSchema,
  timeStampSchema,
  userAttributeSchema,
} from "@/schemas";

const basePublicationSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    shortName: yup.string().required(),
    attributes: yup.array().of(attributeSchema).required(),
    children: yup.array().of(recordAttributeSchema).required(),
    commentCount: yup.number().required(),
    creationTimestamp: timeStampSchema.required(),
    creationUser: userAttributeSchema.required(),
    modificationTimestamp: timeStampSchema.required(),
    modificationUser: userAttributeSchema.required(),
    type: yup.string().optional(),
  })
  .camelCase();

export const publicationSchema = basePublicationSchema.omit(["type"]);

export const publicationAttributeSchema = publicationSchema.omit(["children"]);
