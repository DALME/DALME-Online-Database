import { head } from "ramda";
import * as yup from "yup";

export const taskSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    completed: yup.boolean().required(),
    title: yup.string().required(),
    description: yup.string().required(),
    createdBy: yup.number().required(),
    creationTimestamp: yup.string().required(),
    assignedTo: yup.string().default(null).nullable(),
    owner: yup.string(),
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

export const taskListSchema = yup.array().of(taskSchema);

export const taskListsSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.number().required(),
      group: yup.string().required(),
      name: yup
        .string()
        .transform((value) => {
          const node = document.createElement("html");
          node.innerHTML = value;
          return head(node.getElementsByClassName("mr-auto")).innerText;
        })
        .required(),
      taskCount: yup.number().required(),
      taskIndex: yup.array().of(yup.number().required()).required(),
    })
    .camelCase(),
);
