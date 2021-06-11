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
    assignedTo: yup.string().nullable(),
    owner: yup.string(),
    attachments: yup
      .mixed()
      .nullable()
      .transform((value) => {
        if (value) {
          const node = document.createElement("html");
          node.innerHTML = value;
          const link = head(node.getElementsByTagName("a"));
          return {
            url: link.getAttribute("href"),
            kind: link.innerText,
          };
        }
        return value;
      }),
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
        .required()
        .transform((value) => {
          const node = document.createElement("html");
          node.innerHTML = value;
          return head(node.getElementsByClassName("mr-auto")).innerText;
        }),
      taskCount: yup.number().required(),
      taskIndex: yup.array().of(yup.number()),
    })
    .camelCase(),
);
