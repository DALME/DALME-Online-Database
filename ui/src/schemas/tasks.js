import { DateTime } from "luxon";
import { isNil } from "ramda";
import * as yup from "yup";

import {
  attachmentSchema,
  taskListSchema,
  userAttributeSchema,
  collectionAttributeSchema,
} from "@/schemas";

// Field-level validation rules/schemas.
export const taskFieldValidation = {
  title: yup.string().nullable().required().label("Title"),
  description: yup.string().nullable().required().label("Description"),
  taskList: yup
    .string()
    .nullable()
    .required()
    .transform((option) => {
      return isNil(option) ? null : option.value;
    })
    .label("Task list"),
  dueDate: yup
    .string()
    .nullable()
    .transform((value) => (value ? DateTime.fromISO(value).toISODate() : null))
    .label("Date due"),
  assignedTo: yup
    .object()
    .shape({ value: yup.number().nullable() })
    .nullable()
    .label("Assigned to"),
};

// Edit existing object schema.
export const taskEditSchema = yup.object().shape({
  id: yup.number().required(),
  title: yup.string().required(),
  description: yup.string().required(),
  dueDate: yup
    .string()
    .nullable()
    .transform((value) => (value ? DateTime.fromISO(value).toISODate() : null)),
  assignedTo: yup.string().nullable(),
});

// Full object schema.
export const taskSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    title: yup.string().required(),
    taskList: taskListSchema.shape({
      taskCount: yup.number().default(null).nullable(),
      taskIndex: yup.array().of(yup.number()).default(null).nullable(),
    }),
    description: yup.string().required(),
    dueDate: yup.string().default(null).nullable(),
    completed: yup.boolean().required(),
    completedDate: yup.string().default(null).nullable(),
    completedBy: userAttributeSchema.default(null).nullable(),
    overdue: yup.boolean().default(null).nullable(),
    files: yup.array().of(attachmentSchema).default(null).nullable(),
    resources: yup.array().of(collectionAttributeSchema).default(null).nullable(),
    assignees: yup.array().of(userAttributeSchema).default(null).nullable(),
    url: yup.string().url().default(null).nullable(),
    commentCount: yup.number().default(null).nullable(),
    creationTimestamp: yup.string().required(),
    creationUser: userAttributeSchema.required(),
    modificationTimestamp: yup.string().required(),
    modificationUser: userAttributeSchema.required(),
  })
  .camelCase();

export const tasksSchema = yup.array().of(taskSchema);

// API submit schemas.
export const taskPostSchema = yup.object().shape({});

export const taskPutSchema = taskPostSchema.shape({
  id: yup.number().required(),
});
