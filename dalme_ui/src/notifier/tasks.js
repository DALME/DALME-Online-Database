import { Notify } from "quasar";

const auth = {
  taskStatusUpdated: () =>
    Notify.create({
      color: "green",
      message: "Status updated",
      icon: "done",
      position: "top",
    }),
  taskStatusUpdatedError: () =>
    Notify.create({
      color: "red",
      message: "Status update failed",
      icon: "cancel",
      position: "top",
    }),
};

export default auth;
