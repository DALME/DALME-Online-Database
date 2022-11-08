import { Notify } from "quasar";

const transcriptions = {
  versionCheckFailed: (message) =>
    Notify.create({
      color: "red",
      message: `Transcription version check failed with message "${message}"`,
      position: "top-right",
      icon: "block",
    }),
};

export default transcriptions;
