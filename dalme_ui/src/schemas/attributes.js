import { camelCase } from "camel-case";
import { moment } from "moment";
import * as yup from "yup";

// NOTE: We don't use the usual *Schema naming convention here as it makes
// things easier when we have to do all the dynamic binding/juggling upstream.
// Instead just map it directly to AttributeType.short_name (post-camelization).
export const attributeSchemas = {
  urlAttribute: yup.string().url().nullable().required().label("Web address"),
  mk2Identifier: yup.string().uuid().nullable().required().label("Mk.II ID"),
  mk1Identifier: yup.string().nullable().required().label("Mk.I ID"),
  altIdentifier: yup.string().nullable().required().label("Alt. ID"),
  lastName: yup.string().nullable().required().label("Last name"),
  firstName: yup.string().nullable().required().label("First name"),
  postalCode: yup.string().nullable().required().label("Postal code"),
  poboxNumber: yup.string().nullable().required().label("PO box"),
  streetAddress: yup.string().nullable().required().label("Street address"),
  latitude: yup.string().nullable().required().label("Latitude"),
  longitude: yup.string().nullable().required().label("Longitude"),
  elevation: yup.number().nullable().required().label("Elevation"),
  shortTitle: yup.string().nullable().required().label("Short title"),
  title: yup.string().nullable().required().label("Title"),
  language: yup.number().nullable().required().label("Language (ISO)"), // LanguageReference.id
  languageGc: yup.number().nullable().required().label("Language (GC)"), // LanguageReference.id
  archivalSeries: yup.string().nullable().required().label("Archival series"),
  archivalNumber: yup.string().nullable().required().label("Archival number"),
  date: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD"))
    .label("Date"),
  id: yup.string().nullable().required().label("ID"),
  creationUsername: yup.string().nullable().required().label("Created by"),
  creationTimestamp: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD HH:mm"))
    .label("Created on"),
  modificationUsername: yup.string().nullable().required().label("Modified by"),
  modificationTimestamp: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD HH:mm"))
    .label("Modified on"),
  endDate: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD"))
    .label("End date"),
  startDate: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD"))
    .label("Start date"),
  datasetUsergroup: yup.number().nullable().required().label("DS User Group"),
  recordType: yup.number().nullable().required().label("Record type"),
  recordTypePhrase: yup
    .string()
    .nullable()
    .required()
    .label("Record type phrase"),
  debtPhrase: yup.string().nullable().required().label("Debt phrase"),
  debtAmount: yup.number().nullable().required().label("Debt amount"),
  debtUnit: yup.string().nullable().required().label("Debt unit"),
  debtUnitType: yup.string().nullable().required().label("Debt unit type"),
  debtSource: yup.string().nullable().required().label("Debt source"),
  comments: yup.string().nullable().required().label("Comments"),
  locale: yup.number().nullable().required().label("Locale"), // Locale.id
  namedPersons: yup.string().nullable().required().label("Named persons"), // TODO: Don't think this is right.
  parent: yup.string().nullable().required().label("Parent"),
  hasInventory: yup.boolean().nullable().required().label("List"),
  author: yup.string().nullable().required().label("Author"),
  type: yup.string().nullable().required().label("Type"),
  name: yup.string().nullable().required().label("Name"),
  shortName: yup.string().nullable().required().label("Short name"),
  password: yup.string().nullable().required().label("Password"),
  lastLogin: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD HH:mm"))
    .label("Last login"),
  isSuperuser: yup.boolean().nullable().required().label("Superuser"),
  username: yup.string().nullable().required().label("Username"),
  email: yup.string().email().nullable().required().label("Email"),
  isStaff: yup.boolean().nullable().required().label("Staff"),
  isActive: yup.boolean().nullable().required().label("Active"),
  dateJoined: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD"))
    .label("Date joined"),
  fullName: yup.string().nullable().required().label("Full name"),
  damUser: yup.number().nullable().required().label("DAM user"), // TODO: Options?
  damId: yup.number().nullable().required().label("DAM id"),
  order: yup.number().nullable().required().label("Order"),
  ref: yup.number().nullable().required().label("DAM ID"),
  hasImage: yup.boolean().nullable().required().label("Image"),
  creationDate: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD"))
    .label("Creation date"),
  country: yup.number().nullable().required().label("Country"), // Country.id
  fileSize: yup.number().nullable().required().label("File size"),
  field12: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD"))
    .label("Resource date"),
  field8: yup.string().email().nullable().required().label("Resource title"),
  field3: yup.string().nullable().required().label("Country (RS-DALME)"),
  field51: yup.string().nullable().required().label("Original filename"),
  field79: yup.string().nullable().required().label("Folio"),
  modified: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD"))
    .label("Date modified"),
  groups: yup.string().nullable().required().label("Groups"),
  collections: yup.string().nullable().required().label("Collections"),
  noFolios: yup.number().nullable().required().label("No. folios"),
  createdBy: yup.number().nullable().required().label("Created by (RS)"), // NOTE: Altered to expect user.id
  source: yup.string().nullable().required().label("Source"),
  dataType: yup.string().nullable().required().label("Data type"),
  description: yup.string().nullable().required().label("Description"),
  sameAs: yup.string().nullable().required().label("Same as"), // TODO: This is an ID but not sure how to generate the options for it.
  contentClass: yup.string().nullable().required().label("Content class"),
  attributeTypes: yup.string().nullable().required().label("Attribute types"),
  dtName: yup.string().nullable().required().label("Datatables name"),
  field: yup.number().nullable().required().label("Field"),
  list: yup.number().nullable().required().label("Datatables List"),
  renderExp: yup.string().nullable().required().label("Render expression"),
  orderable: yup.number().nullable().required().label("Orderable"),
  visible: yup.number().nullable().required().label("Visible"),
  searchable: yup.number().nullable().required().label("Searchable"),
  dteName: yup.string().nullable().required().label("DTE name"),
  dteType: yup.string().nullable().required().label("DTE type"),
  dteOptions: yup.string().nullable().required().label("DTE options"),
  dteOpts: yup.string().nullable().required().label("DTE opts"),
  dteMessage: yup.string().nullable().required().label("DTE message"),
  isFilter: yup.boolean().nullable().required().label("Is filter"),
  filterType: yup.string().nullable().required().label("Filter type"),
  filterOptions: yup.string().nullable().required().label("Filter options"),
  filterLookup: yup.string().nullable().required().label("Filter lookup"),
  dtClassName: yup.string().nullable().required().label("DT classname"),
  dtWidth: yup.string().nullable().required().label("DT width"),
  required: yup.boolean().nullable().required().label("Required"),
  optionsList: yup.string().nullable().required().label("Options list"),
  glottocode: yup.string().nullable().required().label("Glottocode"),
  iso6393: yup.string().nullable().required().label("ISO-693-3"),
  status: yup.string().nullable().required().label("Status"),
  result: yup.string().nullable().required().label("Result"),
  dateDone: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD"))
    .label("Date done"),
  traceback: yup.string().nullable().required().label("Traceback"),
  taskName: yup.string().nullable().required().label("Task name"),
  alpha_3Code: yup.string().nullable().required().label("Alpha-3 Code"),
  alpha_2Code: yup.string().nullable().required().label("Alpha-2 Code"),
  numCode: yup.number().nullable().required().label("Numeric code"),
  administrativeRegion: yup
    .string()
    .nullable()
    .required()
    .label("Administrative region"),
  tags: yup.string().nullable().required().label("Tags"),
  subject: yup.string().nullable().required().label("Subject"),
  file: yup.string().nullable().required().label("File"),
  attachments: yup.string().nullable().required().label("Attachments"),
  hasPages: yup.boolean().nullable().required().label("Has pages"),
  parents: yup.string().nullable().required().label("Parents"),
  helpFlag: yup.boolean().nullable().required().label("Help"),
  lastModified: yup
    .string()
    .nullable()
    .required()
    .transform((value) => moment(new Date(value)).format("YYYY-MM-DD HH:mm"))
    .label("Last modified"),
  lastUser: yup.number().nullable().required().label("Last user"), // NOTE: Altered to expect user.id
  activity: yup.string().nullable().required().label("Activity"),
  authority: yup.string().nullable().required().label("Authority"),
  format: yup.string().nullable().required().label("Format"),
  owner: yup.number().nullable().required().label("Owner"), // User.id
  endpoint: yup.string().nullable().required().label("Endpoint"), // TODO: string().url() ?
  progress: yup.string().nullable().required().label("Progress"),
  isPublic: yup.boolean().nullable().required().label("Public"),
  permissions: yup
    .number()
    .min(1)
    .max(4)
    .nullable()
    .required()
    .label("Permissions"),
  setType: yup.number().min(1).max(4).nullable().required().label("Set type"),
  r1Inheritance: yup.string().nullable().required().label("Direct inheritance"),
  r2Inheritance: yup
    .string()
    .nullable()
    .required()
    .label("Indirect inheritance"),
  rightsStatus: yup.string().nullable().required().label("Rights status"),
  rightsNotice: yup.string().nullable().required().label("Rights notice"),
  licence: yup.string().nullable().required().label("Licence"),
  rights: yup.string().nullable().required().label("Rights"),
  rightsHolder: yup.string().nullable().required().label("Rights holder"),
  noticeDisplay: yup
    .boolean()
    .nullable()
    .required()
    .label("Rights notice display"),
  defaultRights: yup
    .string()
    .uuid()
    .nullable()
    .required()
    .label("Default rights"),
  hasLanding: yup.boolean().nullable().required().label("Landing"),
  memberCount: yup.number().min(0).nullable().required().label("Member count"),
  support: yup.string().nullable().required().label("Support"),
  zoteroKey: yup.string().nullable().required().label("Zotero key"),
  legalPersona: yup.string().nullable().required().label("Legal persona"),
  socialStatus: yup.string().nullable().required().label("Social status"),
  religion: yup.string().nullable().required().label("Religion"),
  sex: yup.string().nullable().required().label("Sex"),
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
    optionsList: yup.string().nullable(),
    dataType: yup
      .string()
      .required()
      .when(
        ["shortName", "optionsList", "description"],
        (shortName, optionsList, description, schema) => {
          // Make sure certain fields come through as select fields.
          const forceOptions = [
            "createdBy",
            "lastUser",
            "owner",
            "recordType",
            "sameAs",
          ];
          const optionsType =
            optionsList || forceOptions.includes(shortName) ? "Options" : false;

          // Booleans are a subset of INT so let's sort those out for clarity.
          const booleanType = description.toLowerCase().includes("boolean")
            ? "Boolean"
            : false;

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
                "FK-INT": "Options",
                "FK-UUID": "Options",
              }[value],
          );
        },
      ),
  })
  .camelCase();

export const attributeTypesSchema = yup.array().of(attributeTypeSchema);
