import { last } from "ramda";
import * as yup from "yup";

import { normalizeAttributesOutput } from "@/components/forms/attributes-field/normalize";

import { ownerSchema } from "./common";

export const sourceOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().uuid().required(),
      caption: yup.string().uuid().required(),
    })
    .transform((value) => ({
      label: value.name,
      value: value.id,
      caption: value.id,
    })),
);

const defaultRightsSchema = yup.object().shape({
  name: yup.string().required(),
  url: yup.string().required(),
  id: yup.object().shape({ id: yup.string().uuid().required() }).required(),
});

const localeSchema = yup.object().shape({
  name: yup.string().required(),
  url: yup.string().required(),
  id: yup.object().shape({ id: yup.number().required() }).required(),
});

const primaryDatasetSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    detailString: yup.string().required(),
  })
  .camelCase();

const languageSchema = yup.object().shape({
  name: yup.string().required(),
  url: yup.string().required(),
  id: yup.object().shape({ id: yup.number().required() }).required(),
});

const workflowSchema = yup
  .object()
  .shape({
    helpFlag: yup.boolean().required(),
    isPublic: yup.boolean().required(),
    wfStatus: yup.number().required(),
    stage: yup.number().default(null).nullable(),
    ingestionDone: yup.boolean().required(),
    transcriptionDone: yup.boolean().required(),
    markupDone: yup.boolean().required(),
    reviewDone: yup.boolean().required(),
    parsingDone: yup.boolean().default(null).nullable(),
    activity: yup.object().shape({
      timestamp: yup.string().required(),
      user: yup.string().required(),
      username: yup.string().required(),
    }),
    status: yup.object().shape({ text: yup.string().required() }),
  })
  .camelCase();

const creditSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    type: yup
      .object()
      .shape({ id: yup.number().required(), name: yup.string().required() })
      .required(),
    standardName: yup.string().required(),
    note: yup.string().default(null).nullable(),
  })
  .camelCase();

const setSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    detailString: yup.string().required(),
  })
  .camelCase();

const agentSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    type: yup.string().required(),
    legalPersona: yup.string().default(null).nullable(),
  })
  .camelCase();

const childSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    shortName: yup.string().required(),
    type: yup.string().required(),
    hasInventory: yup.boolean().required(),
  })
  .camelCase();

const objectSchema = yup.object().shape({});

const pageSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    damId: yup.number().default(null).nullable(), // TODO: Unsure if null ok.
    name: yup.string().required(),
    order: yup.number().required(),
    transcriptionId: yup.string().uuid(),
    hasImage: yup.boolean().nullable(),
    hasTranscription: yup.boolean().required(),
  })
  .camelCase();

const placeSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    placename: yup.string().required(),
    locale: yup.string().required(),
  })
  .camelCase();

export const archiveSourceSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    noRecords: yup.number().required(),
    attributes: yup
      .object()
      .shape({
        archiveUrl: yup
          .string()
          .url()
          .default(null)
          .nullable()
          .transform((value) =>
            value.includes(" ") ? `http://${last(value.split(" "))}` : value,
          ),
        locale: localeSchema.default(null).nullable(),
        defaultRights: defaultRightsSchema.default(null).nullable(),
      })
      .required()
      .camelCase(),
  })
  .camelCase();

export const archivalFileSourceSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    primaryDataset: primaryDatasetSchema.required(),
    owner: ownerSchema.required(),
    isPrivate: yup.boolean().required(),
    noRecords: yup.number().required(),
    attributes: yup
      .object()
      .shape({
        locale: yup.array().of(localeSchema).default(null).nullable(),
        authority: yup.string().default(null).nullable(),
        format: yup.string().default(null).nullable(),
        support: yup.string().default(null).nullable(),
      })
      .required(),
  })
  .camelCase();

export const recordSourceSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    noFolios: yup.number().required(),
    owner: ownerSchema.required(),
    isPrivate: yup.boolean().required(),
    workflow: yup
      .object()
      .shape({
        activity: yup.object().shape({
          timestamp: yup.string().required(),
          user: yup.string().required(),
          username: yup.string().required(),
        }),
        helpFlag: yup.boolean().required(),
        isPublic: yup.boolean().required(),
        status: yup.object().shape({ text: yup.string().required() }),
      })
      .required()
      .camelCase(),
    attributes: yup
      .object()
      .shape({
        locale: yup.array().of(localeSchema).default(null).nullable(),
        language: yup.array().of(languageSchema).default(null).nullable(),
        recordType: yup.string().required(),
        date: yup
          .object()
          .shape({ name: yup.string().required() })
          .default(null)
          .nullable(),
        startDate: yup
          .object()
          .shape({ name: yup.string().required() })
          .default(null)
          .nullable(),
        endDate: yup
          .object()
          .shape({ name: yup.string().required() })
          .default(null)
          .nullable(),
      })
      .required()
      .camelCase(),
  })
  .camelCase();

export const bibliographySourceSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    primaryDataset: yup.object().shape({
      id: yup.string().uuid().required(),
      name: yup.string().required(),
    }),
    owner: ownerSchema.required(),
    isPrivate: yup.boolean().required(),
    noRecords: yup.number().required(),
    attributes: yup
      .object()
      .shape({
        defaultRights: defaultRightsSchema.required(),
        zoteroKey: yup.string().default(null).nullable(),
      })
      .camelCase(),
  })
  .camelCase();

export const sourceDetailSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    type: yup
      .object()
      .shape({
        id: yup.number().required(),
        name: yup.string().required(),
      })
      .required(),
    name: yup.string().required(),
    shortName: yup.string().required(),
    parent: yup
      .object()
      .shape({
        id: yup.string().uuid().required(),
        name: yup.string().required(),
      })
      .default(null)
      .nullable(),
    hasInventory: yup.boolean().required(),
    noFolios: yup.number().required(),
    noImages: yup.number().required(),
    noRecords: yup.number().required(),
    isPrivate: yup.boolean().required(),
    owner: ownerSchema.required(),
    primaryDataset: primaryDatasetSchema.default(null).nullable(),
    workflow: workflowSchema.default(null).nullable(),
    created: yup
      .object()
      .shape({
        timestamp: yup.string().required(),
        user: yup.string().required(),
        username: yup.string().required(),
      })
      .required(),
    modified: yup
      .object()
      .shape({
        timestamp: yup.string().required(),
        user: yup.string().required(),
        username: yup.string().required(),
      })
      .default(null)
      .nullable(),
    credits: yup.array().of(creditSchema).default(null).nullable(),
    sets: yup.array().of(setSchema).default(null).nullable(),
    children: yup.array().of(childSchema).default(null).nullable(),
    pages: yup.array().of(pageSchema).default(null).nullable(),
    places: yup.array().of(placeSchema).default(null).nullable(),
    agents: yup.array().of(agentSchema).default(null).nullable(),
    objects: yup.array().of(objectSchema).default(null).nullable(),
    attributes: yup
      .object()
      .shape({
        url: yup
          .string()
          .url()
          .default(null)
          .nullable()
          .transform((value) =>
            value.includes(" ") ? `http://${last(value.split(" "))}` : value,
          ),
        mk1Identifier: yup.number().default(null).nullable(),
        mk2Identifier: yup.string().default(null).nullable(),
        altIdentifier: yup.string().default(null).nullable(),
        archivalSeries: yup.string().default(null).nullable(),
        archivalNumber: yup.number().default(null).nullable(),
        locale: localeSchema.default(null).nullable(),
        recordType: yup.string().default(null).nullable(), // TODO: Really?
        recordTypePhrase: yup.string().default(null).nullable(),
        namedPersons: yup.string().default(null).nullable(),
        description: yup.string().default(null).nullable(),
        debtPhrase: yup.string().default(null).nullable(),
        debtAmount: yup.string().default(null).nullable(),
        debtUnit: yup.string().default(null).nullable(),
        debtSource: yup.string().default(null).nullable(),
        date: yup
          .object()
          .shape({ name: yup.string().required() })
          .default(null)
          .nullable(),
        startDate: yup
          .object()
          .shape({ name: yup.string().required() })
          .default(null)
          .nullable(),
        endDate: yup
          .object()
          .shape({ name: yup.string().required() })
          .default(null)
          .nullable(),
        language: yup
          .array()
          .of(
            yup
              .object()
              .shape({
                name: yup.string().required(),
                url: yup.string().required(),
                id: yup
                  .object()
                  .shape({ id: yup.number().required() })
                  .required(),
              })
              .required(),
          )
          .default(null)
          .nullable(),
        defaultRights: defaultRightsSchema.default(null).nullable(),
        authority: yup.string().default(null).nullable(),
        format: yup.string().default(null).nullable(),
        support: yup.string().default(null).nullable(),
        zoteroKey: yup.string().default(null).nullable(),
      })
      .default(null)
      .nullable()
      .camelCase(),
  })
  .camelCase();

export const sourceListSchema = (sourceType) => {
  const sourceMap = {
    archives: archiveSourceSchema,
    archivalFiles: archivalFileSourceSchema,
    records: recordSourceSchema,
    bibliography: bibliographySourceSchema,
  };
  return yup.object().shape({
    recordsTotal: yup.number().required(),
    recordsFiltered: yup.number().required(),
    data: yup.array().of(sourceMap[sourceType]),
  });
};

// POST/PUT data schemas.
// Normalizes source form data for output to the API.
const sourcePostSchema = yup
  .object()
  .shape({
    name: yup.string().required(),
    shortName: yup.string().required(),
    type: yup.object().shape({
      id: yup.number().nullable().required(),
    }),
    parent: yup
      .object()
      .shape({ id: yup.string().uuid().required() })
      .default(null)
      .nullable(),
    primaryDataset: yup
      .object()
      .shape({ id: yup.string().uuid().required() })
      .default(null)
      .nullable(),
    hasInventory: yup.boolean().default(false).required(),
    isPrivate: yup.boolean().default(false).required(),
    attributes: yup.mixed(), // TODO: We can improve this.
    // sets,
    // agents,
    // credits,
    // pages,
  })
  .transform((data) => {
    return {
      ...data,
      type: { id: data.type.value },
      parent: data.parent ? { id: data.parent.value } : null,
      primaryDataset: data.primaryDataset
        ? { id: data.primaryDataset.value }
        : null,
      hasInventory: Boolean(data.hasInventory),
      isPrivate: Boolean(data.isPrivate),
      attributes: normalizeAttributesOutput(data),
    };
  });

const sourcePutSchema = sourcePostSchema.shape({
  id: yup.string().uuid().required(),
});

export const sourceSubmitSchemas = {
  create: sourcePostSchema,
  update: sourcePutSchema,
};
