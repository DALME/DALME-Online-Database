import { head } from "ramda";
import * as yup from "yup";

export const taskValidator = yup.object().shape({
  title: yup.string().required().label("Title"),
  description: yup.string().required().label("Description"),
  // owner: yup.number().required(), // TODO: Dupe of owner?
  // assignedTo: yup.string().default(null).nullable(),
  // attachments?
});

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
