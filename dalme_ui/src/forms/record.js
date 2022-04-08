import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  AttributesField,
  BooleanField,
  InputField,
  MultipleSelectField,
  SelectField,
} from "@/components/forms";
import {
  attributeValidators,
  recordEditSchema,
  recordFieldValidation,
  recordPostSchema,
  recordPutSchema,
  setOptionsSchema,
  sourceOptionsSchema,
} from "@/schemas";

const recordFormSchema = {
  name: {
    field: "name",
    component: markRaw(InputField),
    label: "Name *",
    description:
      "Name of the source, eg: Inventory of Poncius Gassini (ADBR 3B 57)",
    validation: recordFieldValidation.name,
  },
  shortName: {
    field: "shortName",
    component: markRaw(InputField),
    label: "Short name *",
    description:
      "A short name for the source to use in lists, eg: ADBR 3B 57 (Gassini)",
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
      "Parent record, if applicable, eg: a book for a book chapter, an archival unit for a record, etc.",
    getOptions: () =>
      fetcher(requests.sources.getSourceOptionsByType("records")).then(
        (response) => response.json(),
      ),
    optionsSchema: sourceOptionsSchema,
    validation: recordFieldValidation.parent,
  },
  sets: {
    field: "sets",
    component: markRaw(MultipleSelectField),
    label: "Sets",
    description: "The sets of which the source a member.",
    getOptions: () =>
      fetcher(requests.sets.getSets()).then((response) => response.json()),
    optionsSchema: setOptionsSchema,
    validation: recordFieldValidation.sets,
  },
  attributes: {
    field: "attributes",
    component: markRaw(AttributesField),
    description: "The characteristics of the source.",
    required: ["recordType", "language"],
    // TODO: Constrain by source/set type here.
    validators: attributeValidators,
    validation: recordFieldValidation.attributes,
  },
  // agents: {
  //   field: "agents",
  //   component: markRaw(AgentsField),
  //   description: "People referred to by or involved in the source.",
  //   validators: agentValidators,
  //   validation: recordFieldValidation.agents,
  // },
  // folios: {
  //   field: "folios",
  //   component: markRaw(FoliosField),
  //   description: "The pages/folios contained by the source.",
  //   validators: folioValidators,
  //   validation: recordFieldValidation.folios,
  // },
  // credits: {
  //   field: "credits",
  //   component: markRaw(CreditsField),
  //   description: "Editorial persons who contributed to this source.",
  //   validators: creditValidators,
  //   validation: recordFieldValidation.credits,
  // },
};

// TODO: Wrap these in the normalize out schema?
const recordSubmitSchemas = {
  create: recordPostSchema,
  update: recordPutSchema,
};

const recordRequests = {
  get: (id) => requests.sources.getSource(id),
  // TODO: These two requests don't exist yet.
  create: (data) => requests.sources.createSource(data),
  update: ({ id, ...data }) => requests.sources.editSource(id, data),
};

export default {
  edit: recordEditSchema,
  form: recordFormSchema,
  requests: recordRequests,
  submit: recordSubmitSchemas,
};
