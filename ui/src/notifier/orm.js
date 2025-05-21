import { Notify } from "quasar";

const ORM = {
  warning: (message) =>
    Notify.create({
      color: "yellow",
      position: "top-right",
      icon: "speaker_notes",
      message,
    }),
  error: (message) =>
    Notify.create({
      color: "red",
      position: "top-right",
      icon: "speaker_notes_off",
      message,
    }),
};

export default ORM;
