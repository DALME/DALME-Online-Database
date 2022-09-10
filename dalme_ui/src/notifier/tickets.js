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
  ticketListRetrievalFailed: () =>
    Notify.create({
      color: "red",
      message: "Failed to retrieve list of tickets",
      position: "top-right",
      icon: "block",
    }),
};

export default tickets;
