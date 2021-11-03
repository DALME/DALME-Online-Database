/* Schemas for system list pages. */
import moment from "moment";
import * as yup from "yup";

export const usersSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    fullName: yup.string().required(),
    email: yup.string().email().required(),
    username: yup.string().required(),
    lastLogin: yup
      .string()
      .required()
      .transform((value) =>
        moment(new Date(value)).format("DD-MMM-YYYY HH:mm"),
      ),
    active: yup.boolean().required(),
    staff: yup.boolean().required(),
  })
  .camelCase();

export const localesShema = yup
  .object()
  .shape({
    id: yup.number().required(),
    name: yup.string().required(),
    administrativeRegion: yup.string().required(),
    country: yup.string().required(),
    latitude: yup.number().float().required(),
    longitude: yup.number().float().required(),
  })
  .camelCase();

export const countriesSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    name: yup.string().required(),
    alpha2Code: yup.string().required(),
    alpha3Code: yup.string().required(),
    numericCode: yup.string().required(),
  })
  .camelCase();

export const languagesSchema = yup
  .object()
  .shape({
    id: yup.number().required(),
    name: yup.string().required(),
    glottocode: yup.string().required(),
    iso6393: yup.string().default(null).nullable(),
    type: yup.object().shape({
      id: yup.number().required(),
      name: yup.string().required(),
    }),
    parent: yup.object().shape({
      id: yup.number().required(),
      name: yup.string().required(),
    }),
  })
  .camelCase();
