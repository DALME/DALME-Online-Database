import { isNil } from "ramda";
import * as yup from "yup";

export const recordCreateValidator = yup
  .object()
  .shape({
    name: yup.string().nullable().required().label("Name"),
    shortName: yup.string().nullable().required().label("Short name"),
    list: yup
      .boolean()
      .nullable()
      .required()
      .transform((obj) =>
        isNil(obj) ? null : obj.value === "0" ? false : true,
      )
      .label("List"),
    description: yup.string().nullable().label("Description"),
    owner: yup
      .mixed()
      .nullable()
      .required()
      .transform((value) => value.id)
      .label("Owner"),
    attributes: yup.array().of(yup.mixed()),
  })
  .camelCase();

export const recordUpdateValidator = recordCreateValidator.shape({
  id: yup.string().required().label("ID"),
});

export const recordPostSchema = null;

export const recordPutSchema = null;
