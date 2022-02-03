import { Notify } from "quasar";

const task = {
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
      message: "Task status updated",
      icon: "done",
      position: "top",
    }),
  taskStatusUpdatedError: () =>
    Notify.create({
      color: "red",
      message: "Task status update failed",
      icon: "cancel",
      position: "top",
    }),
};

export default task;
