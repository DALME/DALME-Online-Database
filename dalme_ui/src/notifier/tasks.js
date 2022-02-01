import { Notify } from "quasar";

const auth = {
  taskListDeleted: (name) =>
    Notify.create({
      color: "green",
      message: `Task list "${name}" deleted`,
      icon: "done",
      position: "top",
    }),
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
