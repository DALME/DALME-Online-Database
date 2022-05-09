import { Notify } from "quasar";

const tickets = {
  ticketStatusUpdated: () =>
    Notify.create({
      color: "green",
      message: "Ticket status updated",
      icon: "done",
      position: "bottom-right",
    }),
  ticketStatusUpdatedError: () =>
    Notify.create({
      color: "red",
      message: "Ticket status update failed",
      icon: "cancel",
      position: "bottom-right",
    }),
};

export default tickets;
