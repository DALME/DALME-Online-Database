import { markRaw } from "vue";

import { requests } from "@/api";
import {
  AttributesField,
  InputField,
  SelectField,
  TextField,
} from "@/components/forms";
import { permissionOptions } from "@/forms/constants";
import {
  attributeValidators,
  optionsSchema,
  corpusEditSchema,
  corpusFieldValidation,
  setSubmitSchemas,
} from "@/schemas";

const resourceAttributes = ["endpoint", "hasLanding", "isPublic", "owner"];
const requiredAttributes = null;

const corpusFormSchema = {
  name: {
    field: "name",
    component: markRaw(InputField),
    label: "Name *",
    description: "Name of the set.",
    validation: corpusFieldValidation.name,
  },
  description: {
    field: "description",
    component: markRaw(TextField),
    label: "Description *",
    description: "Information about this set and its purpose.",
    validation: corpusFieldValidation.name,
  },
  permissions: {
    field: "permissions",
    component: markRaw(SelectField),
    label: "Permissions *",
    description: "Define the operations permitted on this set by editors.",
    getOptions: () => new Promise((resolve, _) => resolve(permissionOptions)),
    optionsSchema: optionsSchema,
    validation: corpusFieldValidation.permissions,
  },
  attributes: {
    field: "attributes",
    component: markRaw(AttributesField),
    description: "Required and optional attributes of this set type.",
    allowed: resourceAttributes,
    required: requiredAttributes,
    validators: attributeValidators,
    validation: corpusFieldValidation.attributes,
  },
};

const corpusRequests = {
  get: (id) => requests.sets.getSet(id),
  // TODO: Need to include set_type in here or somewhere else.
  create: (data) => requests.sets.createSet(data),
  update: ({ id, ...data }) => requests.sets.editSet(id, data),
};

export default {
  edit: corpusEditSchema,
  form: corpusFormSchema,
  requests: corpusRequests,
  submit: setSubmitSchemas,
};
