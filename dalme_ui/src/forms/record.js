import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  AgentsField,
  AttributesField,
  BooleanField,
  CreditsField,
  FoliosField,
  InputField,
  MultipleSelectField,
  SelectField,
} from "@/components/forms";
import {
  agentValidators,
  attributeValidators,
  creditValidators,
  folioValidators,
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
    // NOTE: We pass this in here (rather than importing it in the the
    // component) even though it's a monolithic definition and will be the same
    // for all instances of the attributes field. That said, there may be a
    // time on another definition when we want to override some rules, so let's
    // leave that option open.
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
  folios: {
    field: "folios",
    component: markRaw(FoliosField),
    description: "The pages/folios contained by the source.",
    validators: folioValidators,
    validation: recordFieldValidation.folios,
  },
  credits: {
    field: "credits",
    component: markRaw(CreditsField),
    description: "Editorial persons who contributed to this source.",
    validators: creditValidators,
    validation: recordFieldValidation.credits,
  },
};

const recordSubmitSchemas = {
  create: recordPostSchema,
  update: recordPutSchema,
};

const recordRequests = {
  create: (data) => requests.sources.createSource(data),
  update: ({ id, ...data }) => requests.sources.editSource(id, data),
};

export default {
  edit: null, // TODO: Schema here.
  form: recordFormSchema,
  requests: recordRequests,
  submit: recordSubmitSchemas,
};
