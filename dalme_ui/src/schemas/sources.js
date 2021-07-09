import { last } from "ramda";
import * as yup from "yup";

const defaultRightsSchema = yup.object().shape({
  id: yup.string().required(),
  name: yup.string().required(),
  url: yup.string().required(),
});

const localeSchema = yup.object().shape({
  name: yup.string().required(),
  url: yup.string().required(),
});

const ownerSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    username: yup.string().required(),
    fullName: yup.string().required(),
  })
  .camelCase();

export const archiveSourceSchema = yup.object().shape({
  id: yup.string().uuid().required(),
  name: yup.string().required(),
  attributes: yup
    .object()
    .shape({
      url: yup
        .string()
        .url()
        .nullable()
        .transform((value) =>
          value.includes(" ") ? `http://${last(value.split(" "))}` : value,
        ),
      locale: localeSchema.default(null).nullable(),
      defaultRights: defaultRightsSchema.default(null).nullable(),
    })
    .required()
    .camelCase(),
});

export const archivalFileSourceSchema = yup
  .object()
  .shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    primaryDataset: yup
      .object()
      .shape({
        id: yup.string().uuid().required(),
        name: yup.string().required(),
        detailString: yup.string().required(),
      })
      .required()
      .camelCase(),
    owner: ownerSchema.required(),
    isPrivate: yup.boolean().required(),
    noRecords: yup.number().required(),
    attributes: yup
      .object()
      .shape({
        locale: localeSchema.nullable(),
        authority: yup.string().nullable(),
        format: yup.string().nullable(),
        support: yup.string().required(),
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
        locale: localeSchema.nullable(),
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
        language: yup
          .array()
          .of(
            yup
              .object()
              .shape({
                name: yup.string().required(),
                url: yup.string().required(),
              })
              .required(),
          )
          .required(),
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
        zoteroKey: yup.string().required(),
      })
      .camelCase(),
  })
  .camelCase();

export const sourceListSchema = (kind) => {
  const sourceMap = {
    archives: archiveSourceSchema,
    archivalFiles: archivalFileSourceSchema,
    records: recordSourceSchema,
    bibliographies: bibliographySourceSchema,
  };
  return yup.object().shape({
    recordsTotal: yup.number().required(),
    recordsFiltered: yup.number().required(),
    data: yup.array().of(sourceMap[kind]),
  });
};
