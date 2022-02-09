import { markRaw } from "vue";

import { requests } from "@/api";
import { AttributesField, BooleanField, InputField } from "@/components/forms";
import {
  recordCreateValidator,
  recordUpdateValidator,
  recordPostSchema,
  recordPutSchema,
} from "@/schemas";

const recordFormSchema = {
  name: {
    component: markRaw(InputField),
    label: "Name",
    description:
      "Name of the source, eg: Inventory of Poncius Gassini (ADBR 3B 57)",
  },
  shortName: {
    component: markRaw(InputField),
    label: "Short name",
    description:
      "A short name for the source to use in lists, eg: ADBR 3B 57 (Gassini)",
  },
  hasInventory: {
    component: markRaw(BooleanField),
    label: "List",
    description: "Indicates whether this source contains a list of objects.",
  },
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
