import * as yup from "yup";

export const placeListSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.string().uuid().required(),
      standardName: yup.string().required(),
      notes: yup.string().default(null).nullable(),
      locale: yup
        .object()
        .shape({
          objId: yup.number().required(),
          name: yup.string().required(),
          administrativeRegion: yup.string().required(),
          country: yup.string().required(),
        })
        .transformKeys((value) => (value === "id" ? "objId" : value))
        .default(null)
        .nullable()
        .camelCase(),
    })
    .camelCase(),
);
