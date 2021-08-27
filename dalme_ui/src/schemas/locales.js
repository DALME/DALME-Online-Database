import * as yup from "yup";

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
          objId: yup.number().required(),
          name: yup.string().required(),
        })
        .transformKeys((value) => (value === "id" ? "objId" : value))
        .required(),
      latitude: yup.number().required(),
      longitude: yup.number().required(),
    })
    .camelCase(),
);
