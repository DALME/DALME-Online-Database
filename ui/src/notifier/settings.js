import { Notify } from "quasar";

const settings = {
  prefRetrievalFailed: () =>
    Notify.create({
      color: "red",
      message: "Failed to retrieve user preferences",
      position: "top-right",
      icon: "block",
    }),
  prefUpdateFailed: () =>
    Notify.create({
      color: "red",
      message: "Failed to update user preferences",
      position: "top-right",
      icon: "block",
    }),
  prefUpdateSuccess: () =>
    Notify.create({
      color: "green",
      message: "User preferences were updated",
      position: "top-right",
      icon: "speaker_notes",
    }),
  teiElementSetsRetrievalFailed: () =>
    Notify.create({
      color: "red",
      message: "Failed to retrieve user TEI tag setttings",
      position: "top-right",
      icon: "block",
    }),
};

export default settings;
