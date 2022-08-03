import { markRaw } from "vue";

import { requests } from "@/api";
import { AttributesField, InputField } from "@/components/forms";
import {
  attributeValidators,
  archiveEditSchema,
  archiveFieldValidation,
  sourceSubmitSchemas,
} from "@/schemas";

const resourceAttributes = [
  "defaultRights",
  "email",
  "locale",
  "streetAddress",
  "url",
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

const sourceType = { id: 19 }; // TODO: Magic number.
const archiveRequests = {
  get: (id) => requests.sources.getSource(id),
  create: (data) =>
    requests.sources.createSource({ type: sourceType, ...data }),
  update: ({ id, ...data }) =>
    requests.sources.editSource(id, { type: sourceType, ...data }),
};

export default {
  edit: archiveEditSchema,
  form: archiveFormSchema,
  requests: archiveRequests,
  submit: sourceSubmitSchemas,
};
