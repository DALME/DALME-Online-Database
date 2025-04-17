import { camelCase } from "camel-case";
import { isNil } from "ramda";
import * as yup from "yup";

export const attributeDateSchema = yup.object().shape({
  day: yup.number().nullable(),
  month: yup.number().nullable(),
  year: yup.number().nullable(),
  date: yup.date().default(null).nullable(),
  text: yup.string().required(),
});

export const attributeSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup
    .string()
    .required()
    .transform((value) => camelCase(value)),
  label: yup.string().required(),
  description: yup.string().nullable(),
  attributeType: yup.number().required(),
  dataType: yup.string().required(),
  isUnique: yup.boolean().nullable().default(true),
  value: yup
    .mixed()
    .when("dataType", ([dataType], _schema) => {
      switch (dataType) {
        case "BOOL":
          return yup.boolean();
        case "DATE":
          return attributeDateSchema;
        case "FLOAT":
          return yup.number();
        case "FKEY":
          return yup.object();
        case "INT":
          return yup.number();
        case "JSON":
          return yup.mixed();
        default:
          return yup.string();
      }
    })
    .required(),
});

export const attributeListSchema = yup.array().of(attributeSchema);

export const attributesFieldSchema = yup.object().shape({
  attribute: yup
    .object()
    .shape({
      id: yup.number().required(),
      dataType: yup.string().required(),
      shortName: yup.string().required(),
    })
    .required(),
  value: yup.mixed().required(),
});

// Keys mapped to Attribute.short_name (camelized).
export const attributeValidators = {
  // Verified/used.
  archivalNumber: yup.string().nullable().required().label("Archival number"),
  archivalSeries: yup.string().nullable().required().label("Archival series"),
  authority: yup.string().nullable().required().label("Authority"),
  date: yup.date().default(null).nullable().required().label("Date"),
  defaultRights: yup
    .object()
    .shape({ value: yup.string().uuid().required().label("Default rights") })
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : option))
    .label("Default rights"),
  description: yup.string().nullable().required().label("Description"),
  email: yup.string().email().nullable().required().label("Email"),
  endDate: yup.date().default(null).nullable().required().label("End date"),
  format: yup.string().nullable().required().label("Format"),
  hasLanding: yup
    .boolean()
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : Boolean(parseInt(option.value))))
    .label("Has landing"),
  helpFlag: yup
    .boolean()
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : Boolean(parseInt(option.value))))
    .label("Help flag"),
  isPublic: yup
    .boolean()
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : Boolean(parseInt(option.value))))
    .label("Is public"),
  language: yup
    .array()
    .of(yup.object().shape({ value: yup.string().required().label("Language") }))
    .nullable()
    .required()
    .transform((value) => (value && value.length > 0 ? value : null))
    .label("Language"),
  locale: yup
    .object()
    .shape({ value: yup.number().nullable().required().label("Locale") })
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : option))
    .label("Locale"),
  namedPersons: yup.string().nullable().required().label("Named persons"),
  owner: yup
    .object()
    .shape({ value: yup.number().nullable().required().label("Owner") })
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : { ...option, value: parseInt(option.value) }))
    .label("Owner"),
  parent: yup
    .object()
    .shape({ value: yup.string().uuid().nullable().required().label("Parent") })
    .nullable()
    .required()
    .label("Parent"),
  recordType: yup
    .object()
    .shape({ value: yup.string().nullable().required().label("Record type") })
    .nullable()
    .required()
    .label("Record type"),
  startDate: yup.date().default(null).nullable().required().label("Start date"),
  statText: yup.string().nullable().required().label("Stat text"),
  statTitle: yup.string().nullable().required().label("Stat title"),
  status: yup.string().nullable().required().label("Status"),
  streetAddress: yup.string().nullable().required().label("Street address"),
  support: yup.string().nullable().required().label("Support"),
  url: yup.string().url().nullable().required().label("URL"),
  zoteroKey: yup.string().nullable().required().label("Zotero key"),
};

export const attributeTypeSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    name: yup.string().required(),
    shortName: yup
      .string()
      .required()
      .transform((value) => camelCase(value)),
    description: yup.string().nullable(),
    optionsList: yup
      .boolean()
      .nullable()
      .transform((value) => (value ? true : false)),
    dataType: yup
      .string()
      .required()
      .when(["shortName", "optionsList", "description"], (shortName, schema) => {
        // Make sure certain fields come through as select fields.
        const forceOptions = ["createdBy", "endpoint", "lastUser", "owner", "recordType", "sameAs"];
        const optionsType = shortName[1] || forceOptions.includes(shortName[0]) ? "Options" : false;

        // Booleans are a subset of INT so let's sort those out for clarity.
        const booleanType = shortName[2].toLowerCase().includes("boolean") ? "Boolean" : false;

        return schema.transform(
          (value) =>
            optionsType ||
            booleanType ||
            {
              DATE: "Date",
              FLOAT: "Floating Point",
              INT: "Number",
              STR: "String",
              JSON: "Data",
              "FK-INT": "Options",
              "FK-UUID": "Options",
            }[value],
        );
      }),
  })
  .camelCase();

export const attributeTypesSchema = yup.array().of(attributeTypeSchema);
