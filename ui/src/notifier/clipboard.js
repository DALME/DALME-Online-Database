import { Notify } from "quasar";

const clipboard = {
  success: () =>
    Notify.create({
      color: "green",
      message: "The text was copied to the clipboard",
      position: "top-right",
      icon: "speaker_notes",
    }),
  failure: () =>
    Notify.create({
      color: "red",
      message: "The text could not be copied to the clipboard",
      position: "top-right",
      icon: "speaker_notes_off",
    }),
};

export default clipboard;
