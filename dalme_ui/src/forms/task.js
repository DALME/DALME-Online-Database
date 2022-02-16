import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  DateField,
  InputField,
  SelectField,
  TextField,
} from "@/components/forms";
import {
  taskFieldValidation,
  taskListOptionsSchema,
  taskPutSchema,
  taskPostSchema,
  userOptionsSchema,
} from "@/schemas";

const taskFormSchema = {
  title: {
    field: "title",
    component: markRaw(InputField),
    label: "Title *",
    validation: taskFieldValidation.title,
  },
  description: {
    field: "description",
    component: markRaw(TextField),
    label: "Description *",
    validation: taskFieldValidation.description,
  },
  taskList: {
    field: "taskList",
    component: markRaw(SelectField),
    label: "Task list *",
    getOptions: () =>
      fetcher(requests.tasks.taskLists()).then((response) => response.json()),
    optionsSchema: taskListOptionsSchema,
    validation: taskFieldValidation.taskList,
  },
  assignedTo: {
    field: "assignedTo",
    component: markRaw(SelectField),
    label: "Assigned to",
    getOptions: () =>
      fetcher(requests.users.getUsers()).then((response) => response.json()),
    optionsSchema: userOptionsSchema,
    validation: taskFieldValidation.assignedTo,
  },
  dueDate: {
    field: "dueDate",
    component: markRaw(DateField),
    label: "Date due",
    validation: taskFieldValidation.dueDate,
  },
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
  submitSchemas,
};
