import { Notify } from "quasar";

const workflow = {
  updateFailed: () =>
    Notify.create({
      color: "red",
      message: "Failed to update workflow",
      position: "top-right",
      icon: "block",
    }),
};

export default workflow;
