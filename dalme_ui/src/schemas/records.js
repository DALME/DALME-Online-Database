import { isNil } from "ramda";
import * as yup from "yup";

export const recordCreateValidator = yup
  .object()
  .shape({
    name: yup.string().nullable().required().label("Name"),
    shortName: yup.string().nullable().required().label("Short name"),
    hasInventory: yup
      .boolean()
      .nullable()
      .required()
      .transform((obj) =>
        isNil(obj) ? null : [0, "0"].includes(obj.value) ? false : true,
      )
      .label("List"),
    // Here, attributes is omitted as it's handled at the component/field level.
  })
  .camelCase();

export const recordUpdateValidator = recordCreateValidator.shape({
  id: yup.string().required().label("ID"),
});

export const recordPostSchema = null;

export const recordPutSchema = null;
