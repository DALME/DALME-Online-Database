import * as yup from "yup";

export const localeSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    name: yup.string().required(),
    administrativeRegion: yup.string().required(),
    country: yup
      .object()
      .shape({
        id: yup.number().required(),
        name: yup.string().required(),
      })
      .required(),
    latitude: yup.number().required(),
    longitude: yup.number().required(),
  })
  .camelCase();

export const localeListSchema = yup.array().of(localeSchema);
