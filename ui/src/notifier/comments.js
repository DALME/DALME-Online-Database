import { Notify } from "quasar";

const auth = {
  commentAdded: () =>
    Notify.create({
      color: "green",
      message: "Comment added",
      position: "top-right",
      icon: "speaker_notes",
    }),
  commentFailed: () =>
    Notify.create({
      color: "red",
      message: "Comment not added",
      position: "top-right",
      icon: "speaker_notes_off",
    }),
};

export default auth;
