import { camelCase } from "camel-case";
import { DateTime } from "luxon";
import { isNil } from "ramda";
import * as yup from "yup";

export const attributeDateSchema = yup.object().shape({
  day: yup.number().nullable(),
  month: yup.number().nullable(),
  year: yup.number().nullable(),
  date: yup.date().transform((value) => (value == null ? null : new Date(value))),
  text: yup.string().required(),
});

export const attributeSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  label: yup.string().required(),
  description: yup.string().nullable(),
  value: yup
    .mixed()
    .when("dataType", ([dataType], _schema) => {
      switch (dataType) {
        case "BOOL":
          return yup.boolean();
        case "DATE":
          return attributeDateSchema;
        case "DEC":
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
  attributeType: yup.number().required(),
  dataType: yup.string().required(),
});

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
  date: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("Date"),
  defaultRights: yup
    .object()
    .shape({ value: yup.string().uuid().required().label("Default rights") })
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : option))
    .label("Default rights"),
  description: yup.string().nullable().required().label("Description"),
  email: yup.string().email().nullable().required().label("Email"),
  endDate: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("End date"),
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
  startDate: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("Start date"),
  statText: yup.string().nullable().required().label("Stat text"),
  statTitle: yup.string().nullable().required().label("Stat title"),
  status: yup.string().nullable().required().label("Status"),
  streetAddress: yup.string().nullable().required().label("Street address"),
  support: yup.string().nullable().required().label("Support"),
  url: yup.string().url().nullable().required().label("URL"),
  zoteroKey: yup.string().nullable().required().label("Zotero key"),

  // TODO: Temp, remove or move up.
  endpoint: yup
    .object()
    .shape({ value: yup.string().nullable().required().label("Endpoint") })
    .nullable()
    .required()
    .transform((option) => (isNil(option) ? null : option))
    .label("Endpoint"),

  // Unverified/unused.
  activity: yup.string().nullable().required().label("Activity"),
  administrativeRegion: yup.string().nullable().required().label("Administrative region"),
  alpha_2Code: yup.string().nullable().required().label("Alpha-2 Code"),
  alpha_3Code: yup.string().nullable().required().label("Alpha-3 Code"),
  altIdentifier: yup.string().nullable().required().label("Alt. ID"),
  attachments: yup.string().nullable().required().label("Attachments"),
  attributeTypes: yup.string().nullable().required().label("Attribute types"),
  author: yup.string().nullable().required().label("Author"),
  collections: yup.string().nullable().required().label("Collections"),
  comments: yup.string().nullable().required().label("Comments"),
  contentClass: yup.string().nullable().required().label("Content class"),
  country: yup.number().nullable().required().label("Country"),
  createdBy: yup.string().nullable().required().label("Created by (RS)"),
  creationDate: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("Creation date"),
  creationTimestamp: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("Created on"),
  creationUsername: yup.string().nullable().required().label("Created by"),
  damId: yup.number().nullable().required().label("DAM id"),
  damUser: yup.number().nullable().required().label("DAM user"),
  dataType: yup.string().nullable().required().label("Data type"),
  datasetUsergroup: yup.number().nullable().required().label("DS User Group"),
  dateDone: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("Date done"),
  dateJoined: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("Date joined"),
  debtAmount: yup.number().nullable().required().label("Debt amount"),
  debtPhrase: yup.string().nullable().required().label("Debt phrase"),
  debtSource: yup.string().nullable().required().label("Debt source"),
  debtUnit: yup.string().nullable().required().label("Debt unit"),
  debtUnitType: yup.string().nullable().required().label("Debt unit type"),
  dtClassName: yup.string().nullable().required().label("DT classname"),
  dtName: yup.string().nullable().required().label("Datatables name"),
  dtWidth: yup.string().nullable().required().label("DT width"),
  dteMessage: yup.string().nullable().required().label("DTE message"),
  dteName: yup.string().nullable().required().label("DTE name"),
  dteOptions: yup.string().nullable().required().label("DTE options"),
  dteOpts: yup.string().nullable().required().label("DTE opts"),
  dteType: yup.string().nullable().required().label("DTE type"),
  elevation: yup.number().nullable().required().label("Elevation"),
  field12: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("Resource date"),
  field3: yup.string().nullable().required().label("Country (RS-DALME)"),
  field51: yup.string().nullable().required().label("Original filename"),
  field79: yup.string().nullable().required().label("Folio"),
  field8: yup.string().email().nullable().required().label("Resource title"),
  field: yup.number().nullable().required().label("Field"),
  file: yup.string().nullable().required().label("File"),
  fileSize: yup.number().nullable().required().label("File size"),
  filterLookup: yup.string().nullable().required().label("Filter lookup"),
  filterOptions: yup.string().nullable().required().label("Filter options"),
  filterType: yup.string().nullable().required().label("Filter type"),
  firstName: yup.string().nullable().required().label("First name"),
  fullName: yup.string().nullable().required().label("Full name"),
  glottocode: yup.string().nullable().required().label("Glottocode"),
  groups: yup.string().nullable().required().label("Groups"),
  hasImage: yup.boolean().nullable().required().label("Image"),
  hasInventory: yup.boolean().nullable().required().label("List"),
  hasPages: yup.boolean().nullable().required().label("Has pages"),
  id: yup.string().nullable().required().label("ID"),
  isActive: yup.boolean().nullable().required().label("Active"),
  isFilter: yup.boolean().nullable().required().label("Is filter"),
  isStaff: yup.boolean().nullable().required().label("Staff"),
  isSuperuser: yup.boolean().nullable().required().label("Superuser"),
  iso6393: yup.string().nullable().required().label("ISO-693-3"),
  languageGc: yup
    .array()
    .of(yup.object().shape({ value: yup.number().required().label("Language (GC)") }))
    .nullable()
    .required()
    .transform((value) => (value && value.length > 0 ? value : null))
    .label("Language (GC)"),
  lastLogin: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISO())
    .label("Last login"),
  lastModified: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISO())
    .label("Last modified"),
  lastName: yup.string().nullable().required().label("Last name"),
  lastUser: yup.string().nullable().required().label("Last user"),
  latitude: yup.string().nullable().required().label("Latitude"),
  legalPersona: yup.string().nullable().required().label("Legal persona"),
  licence: yup.string().nullable().required().label("Licence"),
  list: yup.number().nullable().required().label("Datatables List"),
  longitude: yup.string().nullable().required().label("Longitude"),
  memberCount: yup.number().min(0).nullable().required().label("Member count"),
  mk1Identifier: yup.number().nullable().required().label("Mk.I ID"),
  mk2Identifier: yup.string().uuid().nullable().required().label("Mk.II ID"),
  modificationTimestamp: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISO())
    .label("Modified on"),
  modificationUsername: yup.string().nullable().required().label("Modified by"),
  modified: yup
    .string()
    .nullable()
    .required()
    .transform((value) => DateTime.fromISO(value).toISODate())
    .label("Date modified"),
  name: yup.string().nullable().required().label("Name"),
  noFolios: yup.number().nullable().required().label("No. folios"),
  noticeDisplay: yup.boolean().nullable().required().label("Rights notice display"),
  numCode: yup.number().nullable().required().label("Numeric code"),
  optionsList: yup.string().nullable().required().label("Options list"),
  order: yup.number().nullable().required().label("Order"),
  orderable: yup.number().nullable().required().label("Orderable"),
  parents: yup.string().nullable().required().label("Parents"),
  password: yup.string().nullable().required().label("Password"),
  permissions: yup
    .object()
    .shape({
      value: yup.number().min(1).max(4).nullable().required().label("Permissions"),
    })
    .label("Permissions"),
  poboxNumber: yup.string().nullable().required().label("PO box"),
  postalCode: yup.string().nullable().required().label("Postal code"),
  progress: yup.string().nullable().required().label("Progress"),
  r1Inheritance: yup.string().nullable().required().label("Direct inheritance"),
  r2Inheritance: yup.string().nullable().required().label("Indirect inheritance"),
  recordTypePhrase: yup.string().nullable().required().label("Record type phrase"),
  ref: yup.number().nullable().required().label("DAM ID"),
  religion: yup.string().nullable().required().label("Religion"),
  renderExp: yup.string().nullable().required().label("Render expression"),
  required: yup.boolean().nullable().required().label("Required"),
  result: yup.string().nullable().required().label("Result"),
  rights: yup.string().nullable().required().label("Rights"),
  rightsHolder: yup.string().nullable().required().label("Rights holder"),
  rightsNotice: yup.string().nullable().required().label("Rights notice"),
  rightsStatus: yup.string().nullable().required().label("Rights status"),
  sameAs: yup.string().nullable().required().label("Same as"),
  searchable: yup.number().nullable().required().label("Searchable"),
  setType: yup.number().min(1).max(4).nullable().required().label("Set type"),
  sex: yup.string().nullable().required().label("Sex"),
  shortName: yup.string().nullable().required().label("Short name"),
  shortTitle: yup.string().nullable().required().label("Short title"),
  socialStatus: yup.string().nullable().required().label("Social status"),
  source: yup.string().nullable().required().label("Source"),
  tags: yup.string().nullable().required().label("Tags"),
  taskName: yup.string().nullable().required().label("Task name"),
  title: yup.string().nullable().required().label("Title"),
  traceback: yup.string().nullable().required().label("Traceback"),
  type: yup.string().nullable().required().label("Type"),
  username: yup.string().nullable().required().label("Username"),
  visible: yup.number().nullable().required().label("Visible"),
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
        console.log(shortName, schema);
        const booleanType = shortName[2].toLowerCase().includes("boolean") ? "Boolean" : false;

        return schema.transform(
          (value) =>
            optionsType ||
            booleanType ||
            {
              DATE: "Date",
              DEC: "Decimal",
              INT: "Number",
              STR: "String",
              TXT: "Text",
              JSON: "Data",
              "FK-INT": "Options",
              "FK-UUID": "Options",
            }[value],
        );
      }),
  })
  .camelCase();

export const attributeTypesSchema = yup.array().of(attributeTypeSchema);
