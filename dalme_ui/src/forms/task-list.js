import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import { InputField, SelectField } from "@/components/forms";
import {
  groupOptionsSchema,
  taskListEditSchema,
  taskListFieldValidation,
  taskListPostSchema,
  taskListPutSchema,
} from "@/schemas";

const taskListFormSchema = {
  name: {
    field: "name",
    component: markRaw(InputField),
    label: "Name *",
    validation: taskListFieldValidation.name,
  },
  group: {
    field: "name",
    component: markRaw(SelectField),
    label: "Group *",
    getOptions: () =>
      fetcher(requests.groups.getGroups()).then((response) => response.json()),
    optionsSchema: groupOptionsSchema,
    validation: taskListFieldValidation.group,
  },
};

const taskListSubmitSchemas = {
  create: taskListPostSchema,
  update: taskListPutSchema,
};

const taskListRequests = {
  create: (data) => requests.tasks.createTaskList(data),
  update: ({ id, ...data }) => requests.tasks.editTaskList(id, data),
};

export default {
  edit: taskListEditSchema,
  form: taskListFormSchema,
  requests: taskListRequests,
  submit: taskListSubmitSchemas,
};
