// Test the use/xstore module.
import { createPinia, defineStore, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it } from "vitest";
import { createMachine } from "xstate";

import { useStoreMachine } from "@/use";

const toggleMachine = createMachine({
  id: "toggle",
  context: {
    count: 0,
  },
  initial: "inactive",
  states: {
    inactive: {
      on: { TOGGLE: "active" },
    },
    active: {
      on: { TOGGLE: "inactive" },
    },
  },
});

const useToggleStore = defineStore(toggleMachine.id, () => useStoreMachine(toggleMachine));

describe("xstore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("toggles", () => {
    const store = useToggleStore();
    expect(store.state.value).toBe("inactive");

    store.send({ type: "TOGGLE" });
    expect(store.state.value).toBe("active");

    store.send({ type: "TOGGLE" });
    expect(store.state.value).toBe("inactive");
  });

  it("captures a persistable snapshot", () => {
    const store = useToggleStore();
    expect(store.state.value).toBe("inactive");
    expect(store.persistable.value).toBe("inactive");

    store.send({ type: "TOGGLE" });
    expect(store.state.value).toBe("active");
    expect(store.persistable.value).toBe("active");
  });
});
