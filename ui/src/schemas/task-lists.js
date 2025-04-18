import { isNil } from "ramda";
import * as yup from "yup";

import { groupSchema, userAttributeSchema } from "@/schemas";

// Full object schema.
export const taskListSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    name: yup.string().required(),
    description: yup.string().nullable(),
    slug: yup.string().required(),
    teamLink: groupSchema.required(),
    owner: userAttributeSchema.required(),
    taskCount: yup.number().required(),
    creationTimestamp: yup.string().required(),
    creationUser: userAttributeSchema.required(),
    modificationTimestamp: yup.string().required(),
    modificationUser: userAttributeSchema.required(),
    // taskIndex: yup.array().of(yup.number().required()).required(),
  })
  .camelCase();

export const taskListsSchema = yup.array().of(taskListSchema);

// Field-level validation rules/schemas.
export const taskListFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  group: yup
    .object()
    .shape({ id: yup.number().nullable().required().label("Group") })
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : { id: option.value }))
    .label("Group"),
};

// Edit existing object schema.
export const taskListEditSchema = yup.object().shape({
  id: yup.number().required(),
  name: yup.string().required(),
  group: yup
    .object()
    .shape({
      value: yup.number().required(),
      label: yup.string().required(),
    })
    .transform((option) => ({ value: option.id, label: option.name }))
    .required(),
});

// API submit schemas.
export const taskListPostSchema = yup
  .object()
  .shape({
    name: yup.string().required(),
    teamLink: yup.number().required(),
  })
  .transform((obj) => ({ ...obj, group: obj.group.value }));

export const taskListPutSchema = taskListPostSchema.shape({
  id: yup.number().required(),
});
