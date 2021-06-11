import * as yup from "yup";

// TODO: This needs filling out somewhat, currently simplified.
export const sourcesSchema = yup.array().of(
  yup.object().shape({
    id: yup.string().uuid().required(),
    name: yup.string().required(),
    short_name: yup.string().required(),
    is_private: yup.boolean().required(),
    no_records: yup.number().required(),
    sets: yup.array(),
    attributes: yup.object(),
    type: yup.object().shape({
      id: yup.number().required(),
      name: yup.string().required(),
    }),
  }),
);
