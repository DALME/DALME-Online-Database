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
    description: "The name of the task list.",
    validation: taskListFieldValidation.name,
  },
  group: {
    field: "group",
    component: markRaw(SelectField),
    label: "Group *",
    description: "Which group is the task list filed under.",
    getOptions: () => fetcher(requests.groups.list()).then((response) => response.json()),
    optionsSchema: groupOptionsSchema,
    validation: taskListFieldValidation.group,
  },
};

const taskListSubmitSchemas = {
  create: taskListPostSchema,
  update: taskListPutSchema,
};

const taskListRequests = {
  create: (data) => requests.taskLists.create(data),
  update: ({ id, ...data }) => requests.tasks.editTaskList(id, data),
};

export default {
  edit: taskListEditSchema,
  form: taskListFormSchema,
  requests: taskListRequests,
  submit: taskListSubmitSchemas,
};
