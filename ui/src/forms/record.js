import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  AgentsField,
  AttributesField,
  BooleanField,
  CreditsField,
  FoliosField,
  InputField,
  // MultipleSelectField,
  SelectField,
} from "@/components/forms";
import {
  agentValidators,
  attributeValidators,
  creditValidators,
  pageValidators,
  recordEditSchema,
  recordFieldValidation,
  recordOptionsSchema,
  recordSubmitSchemas,
} from "@/schemas";

const resourceAttributes = [
  "date",
  "description",
  "endDate",
  "helpFlag",
  "isPublic",
  "language",
  "locale",
  "namedPersons",
  "owner",
  "recordType",
  "startDate",
  "status",
];

const requiredAttributes = ["language", "recordType"];

const recordFormSchema = {
  name: {
    field: "name",
    component: markRaw(InputField),
    label: "Name *",
    description: "Name of the source, eg: Inventory of Poncius Gassini (ADBR 3B 57)",
    validation: recordFieldValidation.name,
  },
  shortName: {
    field: "shortName",
    component: markRaw(InputField),
    label: "Short name *",
    description: "A short name for the source to use in lists, eg: ADBR 3B 57 (Gassini)",
    validation: recordFieldValidation.shortName,
  },
  hasInventory: {
    field: "hasInventory",
    component: markRaw(BooleanField),
    label: "List *",
    description: "Indicates whether this source contains a list of objects.",
    validation: recordFieldValidation.hasInventory,
  },
  parent: {
    field: "parent",
    component: markRaw(SelectField),
    label: "Parent",
    description:
      // eslint-disable-next-line max-len
      "Parent record, if applicable, eg: a book for a book chapter, an archival unit for a record, etc.",
    getOptions: () =>
      fetcher(requests.sources.getSourceOptionsByType("record")).then((response) =>
        response.json(),
      ),
    optionsSchema: recordOptionsSchema,
    validation: recordFieldValidation.parent,
  },
  // sets: {
  //   field: "sets",
  //   component: markRaw(MultipleSelectField),
  //   label: "Sets",
  //   description: "The sets of which the source a member.",
  //   getOptions: () =>
  //     fetcher(requests.sets.getSets()).then((response) => response.json()),
  //   optionsSchema: setOptionsSchema,
  //   validation: recordFieldValidation.sets,
  // },
  attributes: {
    field: "attributes",
    component: markRaw(AttributesField),
    description: "Required and optional attributes of this source type.",
    allowed: resourceAttributes,
    required: requiredAttributes,
    validators: attributeValidators,
    validation: recordFieldValidation.attributes,
  },
  agents: {
    field: "agents",
    component: markRaw(AgentsField),
    description: "People referred to by or involved in the source.",
    validators: agentValidators,
    validation: recordFieldValidation.agents,
  },
  pages: {
    field: "pages",
    component: markRaw(FoliosField),
    description: "The pages/folios contained by the source.",
    validators: pageValidators,
    validation: recordFieldValidation.pages,
  },
  credits: {
    field: "credits",
    component: markRaw(CreditsField),
    description: "Editorial persons who contributed to this source.",
    validators: creditValidators,
    validation: recordFieldValidation.credits,
  },
};

const recordType = { id: 13 }; // TODO: Magic number.
const recordRequests = {
  get: (id) => requests.records.getRecord(id),
  create: (data) => requests.records.createRecord({ type: recordType, ...data }),
  update: ({ id, ...data }) => requests.records.editRecord(id, { type: recordType, ...data }),
};

export default {
  edit: recordEditSchema,
  form: recordFormSchema,
  requests: recordRequests,
  submit: recordSubmitSchemas,
};
