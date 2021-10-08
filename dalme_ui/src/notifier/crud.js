import { Notify } from "quasar";

const CRUD = {
  inlineUpdateSuccess: (info) =>
    Notify.create({
      color: "green",
      message: `${info} updated successfully`,
      position: "top",
      icon: "speaker_notes",
    }),
  inlineUpdateFailed: (info) =>
    Notify.create({
      color: "red",
      message: `Failed to update ${info}`,
      position: "top",
      icon: "speaker_notes_off",
    }),
};

export default CRUD;
