import { head } from "ramda";
import * as yup from "yup";

export const taskListOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().required(),
    })
    .transform((value) => {
      const node = document.createElement("html");
      node.innerHTML = value.name;
      const label = head(node.getElementsByClassName("mr-auto")).innerText;
      return {
        label,
        value: value.id,
        caption: value.group.name,
      };
    }),
);

export const taskListCreateValidator = yup.object().shape({
  name: yup.string().required().label("Name"),
  group: yup.object().nullable().required().label("Group"),
});

export const taskListUpdateValidator = taskListCreateValidator.shape({
  id: yup.string().required().label("ID"),
});

export const taskListPostSchema = taskListCreateValidator.shape({
  group: yup
    .mixed()
    .required()
    .transform((value) => value.id),
});

export const taskListPutSchema = taskListUpdateValidator.shape({
  group: yup
    .mixed()
    .required()
    .transform((value) => value.id),
});

export const taskListSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    group: yup
      .object()
      .shape({ id: yup.number().required(), name: yup.string().required() })
      .required(),
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
  .camelCase();

export const taskListsSchema = yup.array().of(taskListSchema);
