import { Notify } from "quasar";

const auth = {
  authFailed: () =>
    Notify.create({
      color: "red",
      message: "Authentication failed",
      position: "bottom-right",
      icon: "block",
    }),
  logout: () =>
    Notify.create({
      color: "green",
      message: "Logging out",
      position: "bottom-right",
      icon: "exit_to_app",
    }),
  reauthenticated: () =>
    Notify.create({
      color: "green",
      message: "Reauthenticated",
      position: "bottom-right",
      icon: "lock_open",
    }),
};

export default auth;
