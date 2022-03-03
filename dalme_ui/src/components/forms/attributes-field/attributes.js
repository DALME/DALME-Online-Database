import { keys, reduce } from "ramda";
import * as yup from "yup";

import { requests } from "@/api";
import { attributeSchemas } from "@/schemas";

const optionFields = [
  "authority",
  "country",
  "createdBy",
  "defaultRights",
  "format",
  "language",
  "languageGc",
  "lastUser",
  "locale",
  "owner",
  "parent",
  "permissions",
  "recordType",
  "rightsStatus",
  "sameAs",
  "setType",
  "support",
];

const multiple = ["language", "languageGc"];

const optionSchema = yup.object().shape({
  label: yup.string().required(),
  value: yup.string().required(),
  caption: yup.string().default(null).nullable(),
});

const optionsSchema = yup.array().of(optionSchema);

// Tweak the schema here, if necessary to handle data integrity issues.
const alternateSchema = {
  language: yup.array().of(
    optionSchema.shape({
      value: yup
        .string()
        .required()
        .transform((value) => (value === "" ? "mis" : value)),
    }),
  ),
};

export const attributeFields = reduce(
  (obj, attribute) => {
    obj[attribute] = {
      options: optionFields.includes(attribute)
        ? /* eslint-disable */
          {
            request: () => requests.attributes.getAttributeOptions(attribute),
            schema: alternateSchema[attribute] || optionsSchema,
            multiple: multiple.includes(attribute),
          }
        : null,
      /* eslint-enable */
      validation: attributeSchemas[attribute],
    };
    return obj;
  },
  {},
  keys(attributeSchemas),
);