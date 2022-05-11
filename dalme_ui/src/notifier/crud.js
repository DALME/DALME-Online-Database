import { Notify } from "quasar";

const CRUD = {
  success: (message) =>
    Notify.create({
      color: "green",
      position: "top-right",
      icon: "speaker_notes",
      message,
    }),
  failure: (message) =>
    Notify.create({
      color: "red",
      position: "top-right",
      icon: "speaker_notes_off",
      message,
    }),
};

export default CRUD;
