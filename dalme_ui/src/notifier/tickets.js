import { Notify } from "quasar";

const tickets = {
  ticketStatusUpdated: () =>
    Notify.create({
      color: "green",
      message: "Ticket status updated",
      icon: "done",
      position: "top-right",
    }),
  ticketStatusUpdatedError: () =>
    Notify.create({
      color: "red",
      message: "Ticket status update failed",
      icon: "cancel",
      position: "top-right",
    }),
};

export default tickets;
