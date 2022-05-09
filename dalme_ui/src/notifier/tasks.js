import { Notify } from "quasar";

const task = {
  taskListDeleted: (name) =>
    Notify.create({
      color: "green",
      message: `Task list "${name}" deleted`,
      icon: "done",
      position: "bottom-right",
    }),
  taskStatusUpdated: () =>
    Notify.create({
      color: "green",
      message: "Task status updated",
      icon: "done",
      position: "bottom-right",
    }),
  taskStatusUpdatedError: () =>
    Notify.create({
      color: "red",
      message: "Task status update failed",
      icon: "cancel",
      position: "bottom-right",
    }),
};

export default task;
