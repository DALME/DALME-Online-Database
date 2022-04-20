import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  AttributesField,
  InputField,
  MultipleSelectField,
} from "@/components/forms";
import {
  attributeValidators,
  archiveEditSchema,
  archiveFieldValidation,
  setOptionsSchema,
  sourceSubmitSchemas,
} from "@/schemas";

const resourceAttributes = [
  "defaultRights",
  "email",
  "locale",
  "streetAddress",
  "urlAttribute",
];

const requiredAttributes = ["locale"];

const archiveFormSchema = {
  name: {
    field: "name",
    component: markRaw(InputField),
    label: "Name *",
    description:
      "Name of the source, eg: Inventory of Poncius Gassini (ADBR 3B 57)",
    validation: archiveFieldValidation.name,
  },
  shortName: {
    field: "shortName",
    component: markRaw(InputField),
    label: "Short name *",
    description:
      "A short name for the source to use in lists, eg: ADBR 3B 57 (Gassini)",
    validation: archiveFieldValidation.shortName,
  },
  sets: {
    field: "sets",
    component: markRaw(MultipleSelectField),
    label: "Sets",
    description: "The sets of which the source a member.",
    getOptions: () =>
      fetcher(requests.sets.getSets()).then((response) => response.json()),
    optionsSchema: setOptionsSchema,
    validation: archiveFieldValidation.sets,
  },
  attributes: {
    field: "attributes",
    component: markRaw(AttributesField),
    description: "Required and optional attributes of this source type.",
    allowed: resourceAttributes,
    required: requiredAttributes,
    validators: attributeValidators,
    validation: archiveFieldValidation.attributes,
  },
};

const archiveRequests = {
  get: (id) => requests.sources.getSource(id),
  // TODO: Need to include type in here or somewhere else.
  create: (data) => requests.sources.createSource(data),
  update: ({ id, ...data }) => requests.sources.editSource(id, data),
};

export default {
  edit: archiveEditSchema,
  form: archiveFormSchema,
  requests: archiveRequests,
  submit: sourceSubmitSchemas,
};
