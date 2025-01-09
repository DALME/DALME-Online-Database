import * as yup from "yup";

export const preferenceSchema = yup.object().shape({
  name: yup.string().required(),
  label: yup.string().required(),
  description: yup.string().required(),
  dataType: yup.string().required(),
  group: yup.string().required(),
  value: yup
    .mixed()
    .when("dataType", ([dataType], _schema) => {
      switch (dataType) {
        case "BOOL":
          return yup.boolean();
        case "INT":
          return yup.number();
        case "JSON":
          return yup.mixed();
        default:
          return yup.string();
      }
    })
    .required(),
});

export const preferenceListSchema = yup.array().of(preferenceSchema);
