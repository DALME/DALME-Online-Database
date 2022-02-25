import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  DateField,
  InputField,
  SelectField,
  TextField,
} from "@/components/forms";
import {
  taskEditSchema,
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
    description: "The title of the task.",
    validation: taskFieldValidation.title,
  },
  description: {
    field: "description",
    component: markRaw(TextField),
    label: "Description *",
    description: "Explains the nature of the task.",
    validation: taskFieldValidation.description,
  },
  taskList: {
    field: "taskList",
    component: markRaw(SelectField),
    label: "Task list *",
    description: "Designate the category the task is filed under.",
    getOptions: () =>
      fetcher(requests.tasks.taskLists()).then((response) => response.json()),
    optionsSchema: taskListOptionsSchema,
    validation: taskFieldValidation.taskList,
  },
  assignedTo: {
    field: "assignedTo",
    component: markRaw(SelectField),
    label: "Assigned to",
    description: "Who is responsible for the task.",
    getOptions: () =>
      fetcher(requests.users.getUsers()).then((response) => response.json()),
    optionsSchema: userOptionsSchema,
    validation: taskFieldValidation.assignedTo,
  },
  dueDate: {
    field: "dueDate",
    component: markRaw(DateField),
    label: "Date due",
    description: "The task deadline.",
    validation: taskFieldValidation.dueDate,
  },
};

const taskSubmitSchemas = {
  create: taskPostSchema,
  update: taskPutSchema,
};

const taskRequests = {
  create: (data) => requests.tasks.createTask(data),
  update: ({ id, ...data }) => requests.tasks.editTask(id, data),
};

export default {
  edit: taskEditSchema,
  form: taskFormSchema,
  requests: taskRequests,
  submit: taskSubmitSchemas,
};
