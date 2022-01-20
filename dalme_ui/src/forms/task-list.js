import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import { InputField, SelectField } from "@/components/forms";
import {
  groupListSchema,
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
    optionLabel: "name",
    optionsSchema: groupListSchema,
  },
};

const taskListRequests = {
  create: (data) => requests.tasks.createTaskList(data),
  update: ({ id, ...data }) => requests.tasks.editTaskList(id, data),
};

const taskListFormValidators = {
  create: taskListCreateValidator,
  update: taskListUpdateValidator,
};

const submitSchemas = {
  create: taskListPostSchema,
  update: taskListPutSchema,
};

export default {
  requests: taskListRequests,
  schema: taskListFormSchema,
  validators: taskListFormValidators,
  submitSchemas,
};
