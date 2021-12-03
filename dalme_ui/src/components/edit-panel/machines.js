import { createMachine } from "xstate";

export default createMachine({
  id: "EditPanel",
  initial: "normal",
  states: {
    normal: {},
  },
});
