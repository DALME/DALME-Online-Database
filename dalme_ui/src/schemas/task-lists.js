import { isNil } from "ramda";
import * as yup from "yup";
import { groupSchema } from "@/schemas";

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

// Full object schema.
export const taskListSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    group: groupSchema.required(),
    name: yup.string().required(),
    taskCount: yup.number().required(),
    taskIndex: yup.array().of(yup.number().required()).required(),
  })
  .camelCase();

export const taskListsSchema = yup.array().of(taskListSchema);

// API submit schemas.
export const taskListPostSchema = yup
  .object()
  .shape({
    name: yup.string().required(),
    group: yup.number().required(),
  })
  .transform((obj) => ({ ...obj, group: obj.group.value }));

export const taskListPutSchema = taskListPostSchema.shape({
  id: yup.number().required(),
});
