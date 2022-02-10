import { keys, reduce } from "ramda";

import { requests } from "@/api";
import {
  attributeSchemas,
  countryOptionsSchema,
  languageOptionsSchema,
  localeOptionsSchema,
  rightsOptionsSchema,
  sourceOptionsSchema,
  userOptionsSchema,
} from "@/schemas";

const optionsData = {
  createdBy: {
    request: requests.users.getUsers,
    schema: userOptionsSchema,
    multiple: false,
    filterable: true,
  },
  lastUser: {
    request: requests.users.getUsers,
    schema: userOptionsSchema,
    multiple: false,
    filterable: true,
  },
  owner: {
    request: requests.users.getUsers,
    schema: userOptionsSchema,
    multiple: false,
    filterable: true,
  },
  parent: {
    request: requests.sources.getSources,
    schema: sourceOptionsSchema,
    multiple: false,
    filterable: true,
  },
  authority: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
  country: {
    request: requests.countries.getCountries,
    schema: countryOptionsSchema,
    multiple: false,
    filterable: true,
  },
  defaultRights: {
    request: requests.rights.getRights,
    schema: rightsOptionsSchema,
    multiple: false,
    filterable: true,
  },
  format: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
  language: {
    request: requests.languages.getLanguages,
    schema: languageOptionsSchema,
    multiple: true,
    filterable: true,
  },
  languageGc: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
  locale: {
    request: requests.locales.getLocales,
    schema: localeOptionsSchema,
    multiple: false,
    filterable: true,
  },
  permissions: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
  recordType: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
  rightsStatus: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
  sameAs: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
  setType: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
  support: {
    request: null,
    schema: null,
    multiple: false,
    filterable: true,
  },
};

export const attributeFields = reduce(
  (obj, attribute) => {
    obj[attribute] = {
      options: optionsData[attribute] || null,
      validation: attributeSchemas[attribute],
    };
    return obj;
  },
  {},
  keys(attributeSchemas),
);
