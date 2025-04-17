import { Notify } from "quasar";

const editor = {
  teiElementSetsRetrievalFailed: () =>
    Notify.create({
      color: "red",
      message: "Failed to retrieve user TEI tag setttings",
      position: "top-right",
      icon: "block",
    }),
};

export default editor;
