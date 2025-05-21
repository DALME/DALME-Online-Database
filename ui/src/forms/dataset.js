import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import { AttributesField, InputField, SelectField, TextField } from "@/components/forms";
import { permissionOptions } from "@/forms/constants";
import {
  attributeValidators,
  datasetEditSchema,
  datasetFieldValidation,
  groupOptionsSchema,
  optionsSchema,
} from "@/schemas";

const resourceAttributes = ["endpoint", "owner"];
const requiredAttributes = null;

const datasetFormSchema = {
  name: {
    field: "name",
    component: markRaw(InputField),
    label: "Name *",
    description: "Name of the set.",
    validation: datasetFieldValidation.name,
  },
  description: {
    field: "description",
    component: markRaw(TextField),
    label: "Description *",
    description: "Information about this set and its purpose.",
    validation: datasetFieldValidation.name,
  },
  permissions: {
    field: "permissions",
    component: markRaw(SelectField),
    label: "Permissions *",
    description: "Define the operations permitted on this set by editors.",
    getOptions: () => new Promise((resolve, _) => resolve(permissionOptions)),
    optionsSchema: optionsSchema,
    validation: datasetFieldValidation.parent,
  },
  datasetUsergroup: {
    field: "datasetUsergroup",
    component: markRaw(SelectField),
    label: "Dataset group *",
    description: "User group to be linked with this set.",
    getOptions: () => fetcher(requests.groups.getByDataset()).then((response) => response.json()),
    optionsSchema: groupOptionsSchema,
    validation: datasetFieldValidation.datasetUsergroup,
  },
  attributes: {
    field: "attributes",
    component: markRaw(AttributesField),
    description: "Required and optional attributes of this set type.",
    allowed: resourceAttributes,
    required: requiredAttributes,
    validators: attributeValidators,
    validation: datasetFieldValidation.attributes,
  },
};

const setType = { id: 3 }; // TODO: Magic number.
const datasetRequests = {
  get: (id) => requests.sets.getSet(id),
  create: (data) => requests.sets.createSet({ setType, ...data }),
  update: ({ id, ...data }) => requests.sets.editSet(id, { setType, ...data }),
};

export default {
  edit: datasetEditSchema,
  form: datasetFormSchema,
  requests: datasetRequests,
};
