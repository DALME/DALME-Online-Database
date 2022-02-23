import { head } from "ramda";
import * as yup from "yup";

// Object to select/option transformation schema.
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

// Field-level validation rules/schemas.
export const taskListFieldValidation = {
  name: yup.string().nullable().required().label("Name"),
  group: yup.number().nullable().required().label("Group"),
};

// Edit existing object schema.
// In this case it's not needed (we do everything inline as we don't need to
// call out for the data) but define it here to preserve the overall symmetry.
export const taskListEditSchema = null;

// Full object schema.
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

// API submit schemas.
export const taskListPostSchema = yup.object().shape({
  name: yup.string().required(),
  group: yup
    .mixed() // Number barfs with NaN.
    .required()
    .transform((option) => {
      return option.value;
    }),
});

export const taskListPutSchema = taskListPostSchema.shape({
  id: yup.number().required(),
});
