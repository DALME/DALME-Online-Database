import { Notify } from "quasar";

const records = {
  addAttributeFailed: (name) =>
    Notify.create({
      color: "red",
      message: `Failed to add new attribute: '${name}'`,
      position: "top-right",
      icon: "block",
    }),
  fieldUpdateFailed: (field) =>
    Notify.create({
      color: "red",
      message: `Failed to update field: '${field}'`,
      position: "top-right",
      icon: "block",
    }),
};

export default records;
