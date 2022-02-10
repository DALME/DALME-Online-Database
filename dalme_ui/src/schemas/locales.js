import * as yup from "yup";

export const localeOptionsSchema = yup.array().of(
  yup
    .object()
    .shape({
      label: yup.string().required(),
      value: yup.string().required(),
      caption: yup.string().required(),
    })
    .transform((value) => ({
      label: value.nam,
      value: value.id,
      caption: value.country.name,
    })),
);

export const localeListSchema = yup.array().of(
  yup
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
    .camelCase(),
);
