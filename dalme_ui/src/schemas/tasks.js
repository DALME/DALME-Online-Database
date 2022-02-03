import moment from "moment";
import { head } from "ramda";
import * as yup from "yup";

import { taskListSchema } from "@/schemas";

export const taskCreateValidator = yup.object().shape({
  title: yup.string().nullable().required().label("Title"),
  description: yup.string().nullable().required().label("Description"),
  taskList: taskListSchema
    .shape({
      name: yup.string().required(),
    })
    .nullable()
    .required()
    .label("Task list"),
  dueDate: yup
    .string()
    .nullable()
    .transform((value) =>
      value ? moment(new Date(value)).format("YYYY-MM-DD") : null,
    )
    .label("Date due"),
});

export const taskUpdateValidator = taskCreateValidator.shape({
  id: yup.string().required().label("ID"),
});

export const taskPostSchema = taskCreateValidator.shape({
  taskList: yup
    .mixed()
    .required()
    .transform((value) => ({ group: value.id, name: value.name })),
  assignedTo: yup
    .mixed()
    .required()
    .transform((value) => value.id),
});

export const taskPutSchema = taskUpdateValidator;

export const taskSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    assignedTo: yup.string().required(),
    completed: yup.boolean().required(),
    title: yup.string().required(),
    description: yup.string().required(),
    completedDate: yup.string().default(null).nullable(),
    createdBy: yup.number().required(),
    creationTimestamp: yup.string().required(),
    dueDate: yup.string().default(null).nullable(),
    taskList: taskListSchema.shape({
      taskCount: yup.number().default(null).nullable(),
      taskIndex: yup.array().of(yup.number()).default(null).nullable(),
    }),
    creationUser: yup
      .object()
      .shape({
        id: yup.number().required(),
        username: yup.string().required(),
        fullName: yup.string().required(),
        avatar: yup.string().url().default(null).nullable(),
      })
      .camelCase(),
    attachments: yup
      .mixed()
      .transform((value) => {
        if (value) {
          const node = document.createElement("html");
          node.innerHTML = value;
          const link = head(node.getElementsByTagName("a"));
          const url = link.getAttribute("href");
          const kind = link.innerText;
          return { url, kind };
        }
        return value;
      })
      .default(null)
      .nullable(),
  })
  .camelCase();

export const tasksSchema = yup.array().of(taskSchema);
