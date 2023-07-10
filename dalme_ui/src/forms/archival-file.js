import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import { AttributesField, InputField, SelectField } from "@/components/forms";
import {
  attributeValidators,
  archivalFileEditSchema,
  archivalFileFieldValidation,
  setOptionsSchema,
  sourceOptionsSchema,
  sourceSubmitSchemas,
} from "@/schemas";

const resourceAttributes = [
  "authority",
  "format",
  "support",
  "archivalNumber",
  "archivalSeries",
  "isPrivate",
  "locale",
  "owner",
  "startDate",
  "endDate",
];

const requiredAttributes = ["authority", "format", "support"];

const archivalFileFormSchema = {
  name: {
    field: "name",
    component: markRaw(InputField),
    label: "Name *",
    description: "Name of the source, eg: Inventory of Poncius Gassini (ADBR 3B 57)",
    validation: archivalFileFieldValidation.name,
  },
  shortName: {
    field: "shortName",
    component: markRaw(InputField),
    label: "Short name *",
    description: "A short name for the source to use in lists, eg: ADBR 3B 57 (Gassini)",
    validation: archivalFileFieldValidation.shortName,
  },
  parent: {
    field: "parent",
    component: markRaw(SelectField),
    label: "Parent",
    description:
      // eslint-disable-next-line max-len
      "Parent record, if applicable, eg: a book for a book chapter, an archival unit for a record, etc.",
    getOptions: () =>
      fetcher(requests.sources.getSourceOptionsByType("archivalFile")).then((response) =>
        response.json(),
      ),
    optionsSchema: sourceOptionsSchema,
    validation: archivalFileFieldValidation.parent,
  },
  primaryDataset: {
    field: "primaryDataset",
    component: markRaw(SelectField),
    label: "Primary dataset",
    description: "Dataset used to assign permissions.",
    getOptions: () => fetcher(requests.sets.getSetsByType(3)).then((response) => response.json()),
    optionsSchema: setOptionsSchema,
    validation: archivalFileFieldValidation.primaryDataset,
  },
  attributes: {
    field: "attributes",
    component: markRaw(AttributesField),
    description: "Required and optional attributes of this source type.",
    allowed: resourceAttributes,
    required: requiredAttributes,
    validators: attributeValidators,
    validation: archivalFileFieldValidation.attributes,
  },
};

const archivalFileRequests = {
  get: (id) => requests.sources.getSource(id),
  // TODO: Need to include type in here or somewhere else.
  create: (data) => requests.sources.createSource(data),
  update: ({ id, ...data }) => requests.sources.editSource(id, data),
};

export default {
  edit: archivalFileEditSchema,
  form: archivalFileFormSchema,
  requests: archivalFileRequests,
  submit: sourceSubmitSchemas,
};
