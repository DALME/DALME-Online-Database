import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  AttributesField,
  BooleanField,
  InputField,
  MultipleSelectField,
} from "@/components/forms";
import {
  pageOptionsSchema,
  recordCreateValidator,
  recordUpdateValidator,
  recordPostSchema,
  recordPutSchema,
  setOptionsSchema,
} from "@/schemas";

const recordFormSchema = {
  name: {
    component: markRaw(InputField),
    label: "Name *",
    description:
      "Name of the source, eg: Inventory of Poncius Gassini (ADBR 3B 57)",
  },
  shortName: {
    component: markRaw(InputField),
    label: "Short name *",
    description:
      "A short name for the source to use in lists, eg: ADBR 3B 57 (Gassini)",
  },
  hasInventory: {
    component: markRaw(BooleanField),
    label: "List *",
    description: "Indicates whether this source contains a list of objects.",
  },
  pages: {
    component: markRaw(MultipleSelectField),
    label: "Folios",
    description: "The pages/folios contained by the source",
    filterable: true,
    getOptions: () =>
      fetcher(requests.pages.getPages()).then((response) => response.json()),
    optionsSchema: pageOptionsSchema,
  },
  sets: {
    component: markRaw(MultipleSelectField),
    label: "Sets",
    description: "The sets of which the source a member.",
    filterable: true,
    getOptions: () =>
      fetcher(requests.sets.getSets()).then((response) => response.json()),
    optionsSchema: setOptionsSchema,
  },
  // credits
  attributes: {
    component: markRaw(AttributesField),
    required: ["parent", "recordType", "language"],
  },
};

const recordFormValidators = {
  create: recordCreateValidator,
  update: recordUpdateValidator,
};

const submitSchemas = {
  create: recordPostSchema,
  update: recordPutSchema,
};

const recordRequests = {
  create: (data) => requests.sources.createSource(data),
  update: ({ id, ...data }) => requests.sources.editSource(id, data),
};

export default {
  requests: recordRequests,
  schema: recordFormSchema,
  validators: recordFormValidators,
  submitSchemas,
};
