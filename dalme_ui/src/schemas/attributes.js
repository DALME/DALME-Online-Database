import { camelCase } from "camel-case";
import { isNil } from "ramda";
import * as yup from "yup";

export const attributeSchemas = {
  urlAttributeSchema: yup
    .string()
    .url()
    .nullable()
    .required()
    .label("Web address"),
  mk2IdentifierSchema: yup
    .string()
    .uuid()
    .nullable()
    .required()
    .label("Mk.II ID"),
  mk1Identifier: yup.string().nullable().required().label("Mk.I ID"),
  altIdentifier: yup.string().nullable().required().label("Alt. ID"),
  lastName: yup.string().nullable().required().label("Last name"),
  firstName: yup.string().nullable().required().label("First name"),
};
// export const postalCode
// export const poboxNumber
// export const streetAddress
// export const latitude
// export const longitude
// export const elevation
// export const shortTitle
// export const title
// export const language
// export const languageGc
// export const archivalSeries
// export const archivalNumber
// export const date
// export const id
// export const creationUsername
// export const creationTimestamp
// export const modificationUsername
// export const modificationTimestamp
// export const endDate
// export const startDate
// export const datasetUsergroup
// export const recordType
// export const recordTypePhrase
// export const debtPhrase
// export const debtAmount
// export const debtUnit
// export const debtUnitType
// export const debtSource
// export const comments
// export const locale
// export const namedPersons
// export const parent
// export const hasInventory
// export const author
// export const type
// export const name
// export const shortName
// export const password
// export const lastLogin
// export const isSuperuser
// export const username
// export const email
// export const isStaff
// export const isActive
// export const dateJoined
// export const fullName
// export const damUser
// export const damId
// export const order
// export const ref
// export const hasImage
// export const creationDate
// export const country
// export const fileSize
// export const field12
// export const field8
// export const field3
// export const field51
// export const field79
// export const modified
// export const groups
// export const collections
// export const noFolios
// export const createdBy
// export const source
// export const dataType
// export const description
// export const sameAs
// export const contentClass
// export const attributeTypes
// export const dtName
// export const field
// export const list
// export const renderExp
// export const orderable
// export const visible
// export const searchable
// export const dteName
// export const dteType
// export const dteOptions
// export const dteOpts
// export const dteMessage
// export const isFilter
// export const filterType
// export const filterOptions
// export const filterLookup
// export const dtClassName
// export const dtWidth
// export const required
// export const optionsList
// export const glottocode
// export const iso6393
// export const status
// export const result
// export const dateDone
// export const traceback
// export const taskName
// export const alpha_3Code
// export const alpha_2Code
// export const numCode
// export const administrativeRegion
// export const tags
// export const subject
// export const file
// export const attachments
// export const hasPages
// export const parents
// export const helpFlag
// export const lastModified
// export const lastUser
// export const activity
// export const authority
// export const format
// export const owner
// export const endpoint
// export const progress
// export const isPublic
// export const permissions
// export const setType
// export const r1Inheritance
// export const r2Inheritance
// export const rightsStatus
// export const rightsNotice
// export const licence
// export const rights
// export const rightsHolder
// export const noticeDisplay
// export const defaultRights
// export const hasLanding
// export const memberCount
// export const support
// export const zoteroKey
// export const legalPersona
// export const socialStatus
// export const religion
// export const sex

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
    dataType: yup
      .string()
      .required()
      .when(
        ["optionsList", "description"],
        (optionsList, description, schema) => {
          // If the record has options, then use those, no matter the type.
          const optionsType = isNil(optionsList) ? false : "Options";
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

export const attributeValueSchema = yup.mixed().nullable().required();
