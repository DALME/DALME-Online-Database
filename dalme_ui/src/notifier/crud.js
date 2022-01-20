import { Notify } from "quasar";

const CRUD = {
  success: (message) =>
    Notify.create({
      color: "green",
      position: "top",
      icon: "speaker_notes",
      message,
    }),
  failure: (message) =>
    Notify.create({
      color: "red",
      position: "top",
      icon: "speaker_notes_off",
      message,
    }),
};

export default CRUD;
