import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import { InputField, SelectField } from "@/components/forms";
import {
  groupOptionsSchema,
  taskListCreateValidator,
  taskListUpdateValidator,
  taskListPostSchema,
  taskListPutSchema,
} from "@/schemas";

const taskListFormSchema = {
  name: {
    component: markRaw(InputField),
    label: "Name",
  },
  group: {
    component: markRaw(SelectField),
    label: "Group",
    getOptions: () =>
      fetcher(requests.groups.getGroups()).then((response) => response.json()),
    optionsSchema: groupOptionsSchema,
  },
};

const taskListFormValidators = {
  create: taskListCreateValidator,
  update: taskListUpdateValidator,
};

const submitSchemas = {
  create: taskListPostSchema,
  update: taskListPutSchema,
};

const taskListRequests = {
  create: (data) => requests.tasks.createTaskList(data),
  update: ({ id, ...data }) => requests.tasks.editTaskList(id, data),
};

export default {
  requests: taskListRequests,
  schema: taskListFormSchema,
  validators: taskListFormValidators,
  submitSchemas,
};
