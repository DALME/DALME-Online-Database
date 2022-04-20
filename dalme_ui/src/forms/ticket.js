import { markRaw } from "vue";
import { fetcher, requests } from "@/api";
import {
  InputField,
  MultipleSelectField,
  SelectField,
  TextField,
} from "@/components/forms";
import { statusOptions, ticketTagOptions } from "@/forms/constants";
import {
  ticketTagOptionsSchema,
  ticketEditSchema,
  ticketFieldValidation,
  ticketSubmitSchemas,
  ticketStatusOptionsSchema,
  userOptionsSchema,
} from "@/schemas";

const ticketFormSchema = {
  subject: {
    field: "subject",
    component: markRaw(InputField),
    label: "Subject *",
    description: "The subject of the ticket.",
    validation: ticketFieldValidation.subject,
  },
  description: {
    field: "description",
    component: markRaw(TextField),
    label: "Description *",
    description: "Explains the nature of the ticket.",
    validation: ticketFieldValidation.description,
  },
  status: {
    field: "status",
    component: markRaw(SelectField),
    label: "Status",
    description: "Is the ticket open or closed.",
    getOptions: () => new Promise((resolve, _) => resolve(statusOptions)),
    optionsSchema: ticketStatusOptionsSchema,
    validation: ticketFieldValidation.status,
  },
  assignedTo: {
    field: "assignedTo",
    component: markRaw(SelectField),
    label: "Assigned to",
    description: "Who is responsible for the ticket.",
    getOptions: () =>
      fetcher(requests.users.getUsers()).then((response) => response.json()),
    optionsSchema: userOptionsSchema,
    validation: ticketFieldValidation.assignedTo,
  },
  tags: {
    field: "tags",
    component: markRaw(MultipleSelectField),
    label: "Tags",
    description: "What categories the ticket falls into.",
    getOptions: () => new Promise((resolve, _) => resolve(ticketTagOptions)),
    optionsSchema: ticketTagOptionsSchema,
    validation: ticketFieldValidation.tags,
  },
  // url -> URL field consult Gabe quasar branch
  // file -> upload field consult Gabe quasar branch
};

const ticketRequests = {
  get: (id) => requests.tickets.getTicket(id),
  create: (data) => requests.tickets.createTicket(data),
  update: ({ id, ...data }) => requests.tickets.editTicket(id, data),
};

export default {
  edit: ticketEditSchema,
  form: ticketFormSchema,
  requests: ticketRequests,
  submit: ticketSubmitSchemas,
};
