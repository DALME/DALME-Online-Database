import { Notify } from "quasar";

const users = {
  userListRetrievalFailed: () =>
    Notify.create({
      color: "red",
      message: "Failed to retrieve list of users",
      position: "top-right",
      icon: "block",
    }),
};

export default users;
