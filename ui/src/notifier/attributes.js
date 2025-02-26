import { Notify } from "quasar";

const attributes = {
  updateFailed: (name) =>
    Notify.create({
      color: "red",
      message: `Failed to update attribute: '${name}'`,
      position: "top-right",
      icon: "block",
    }),
};

export default attributes;
