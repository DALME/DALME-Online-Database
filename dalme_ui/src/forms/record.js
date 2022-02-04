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
  },
  shortName: {
    component: markRaw(InputField),
    label: "Short name",
  },
  hasInventory: {
    component: markRaw(BooleanField),
    label: "List",
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
