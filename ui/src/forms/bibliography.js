import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import { AttributesField, InputField, SelectField } from "@/components/forms";
import {
  attributeValidators,
  bibliographyEditSchema,
  bibliographyFieldValidation,
  bibliographyTypeOptionsSchema,
  recordSubmitSchemas,
} from "@/schemas";

const resourceAttributes = ["defaultRights", "isPrivate", "owner", "parent", "zoteroKey"];

const requiredAttributes = ["defaultRights", "zoteroKey"];

const bibliographyFormSchema = {
  name: {
    field: "name",
    component: markRaw(InputField),
    label: "Name *",
    description: "Name of the source, eg: Inventory of Poncius Gassini (ADBR 3B 57)",
    validation: bibliographyFieldValidation.name,
  },
  shortName: {
    field: "shortName",
    component: markRaw(InputField),
    label: "Short name *",
    description: "A short name for the source to use in lists, eg: ADBR 3B 57 (Gassini)",
    validation: bibliographyFieldValidation.shortName,
  },
  type: {
    field: "type",
    component: markRaw(SelectField),
    label: "Bilbliography type *",
    description: "The category of bibliography for this source.",
    getOptions: () =>
      fetcher(requests.sources.getBibliographyTypes()).then((response) => response.json()),
    optionsSchema: bibliographyTypeOptionsSchema,
    validation: bibliographyFieldValidation.type,
  },
  attributes: {
    field: "attributes",
    component: markRaw(AttributesField),
    description: "Required and optional attributes of this source type.",
    allowed: resourceAttributes,
    required: requiredAttributes,
    validators: attributeValidators,
    validation: bibliographyFieldValidation.attributes,
  },
};

const bibliographyRequests = {
  get: (id) => requests.sources.getSource(id),
  create: (data) => requests.sources.createSource(data),
  update: ({ id, ...data }) => requests.sources.editSource(id, data),
};

export default {
  edit: bibliographyEditSchema,
  form: bibliographyFormSchema,
  requests: bibliographyRequests,
  submit: recordSubmitSchemas,
};
