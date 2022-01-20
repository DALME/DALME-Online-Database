import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  DateField,
  InputField,
  SelectField,
  TextField,
} from "@/components/forms";
import {
  taskListsSchema,
  taskPutSchema,
  taskPostSchema,
  taskCreateValidator,
  taskUpdateValidator,
} from "@/schemas";

const taskFormSchema = {
  title: {
    component: markRaw(InputField),
    label: "Title",
  },
  description: {
    component: markRaw(TextField),
    label: "Description",
  },
  taskList: {
    component: markRaw(SelectField),
    label: "Task list",
    getOptions: () =>
      fetcher(requests.tasks.taskLists()).then((response) => response.json()),
    optionLabel: (option) => `${option.name} (${option.group})`,
    optionsSchema: taskListsSchema,
  },
  dueDate: {
    component: markRaw(DateField),
    label: "Date due",
  },
};

const taskRequests = {
  create: (data) => requests.tasks.createTask(data),
  update: ({ id, ...data }) => requests.tasks.editTask(id, data),
};

const taskFormValidators = {
  create: taskCreateValidator,
  update: taskUpdateValidator,
};

const submitSchemas = {
  create: taskPostSchema,
  update: taskPutSchema,
};

export default {
  requests: taskRequests,
  schema: taskFormSchema,
  validators: taskFormValidators,
  submitSchemas,
};
