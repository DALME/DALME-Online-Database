import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  DateField,
  InputField,
  SelectField,
  TextField,
} from "@/components/forms";
import {
  taskListOptionsSchema,
  taskPutSchema,
  taskPostSchema,
  taskCreateValidator,
  taskUpdateValidator,
  userOptionsSchema,
} from "@/schemas";

const taskFormSchema = {
  title: {
    component: markRaw(InputField),
    label: "Title *",
  },
  description: {
    component: markRaw(TextField),
    label: "Description *",
  },
  taskList: {
    component: markRaw(SelectField),
    label: "Task list *",
    filterable: true,
    getOptions: () =>
      fetcher(requests.tasks.taskLists()).then((response) => response.json()),
    optionsSchema: taskListOptionsSchema,
  },
  assignedTo: {
    component: markRaw(SelectField),
    label: "Assigned to",
    filterable: true,
    getOptions: () =>
      fetcher(requests.users.getUsers()).then((response) => response.json()),
    optionsSchema: userOptionsSchema,
  },
  dueDate: {
    component: markRaw(DateField),
    label: "Date due",
  },
};

const taskFormValidators = {
  create: taskCreateValidator,
  update: taskUpdateValidator,
};

const submitSchemas = {
  create: taskPostSchema,
  update: taskPutSchema,
};

const taskRequests = {
  create: (data) => requests.tasks.createTask(data),
  update: ({ id, ...data }) => requests.tasks.editTask(id, data),
};

export default {
  requests: taskRequests,
  schema: taskFormSchema,
  validators: taskFormValidators,
  submitSchemas,
};
