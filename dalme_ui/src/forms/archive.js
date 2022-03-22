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
  archivePutSchema,
  archivePostSchema,
  setOptionsSchema,
} from "@/schemas";

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
    required: ["locale"],
    // NOTE: We pass this in here (rather than importing it in the the
    // component) even though it's a monolithic definition and will be the same
    // for all instances of the attributes field. That said, there may be a
    // time we want to override some rules, so let's leave that option open.
    validators: attributeValidators,
    validation: archiveFieldValidation.attributes,
  },
};

const archiveSubmitSchemas = {
  create: archivePostSchema,
  update: archivePutSchema,
};

const archiveRequests = {
  create: (data) => requests.archives.createSource(data),
  update: ({ id, ...data }) => requests.archives.editSource(id, data),
};

export default {
  edit: archiveEditSchema,
  form: archiveFormSchema,
  requests: archiveRequests,
  submit: archiveSubmitSchemas,
};
