import * as yup from "yup";

const sessionSchema = yup.object().shape({
  id: yup.number().required(),
  username: yup.string().required(),
});

export { sessionSchema };
