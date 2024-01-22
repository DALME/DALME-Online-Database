// Allow xstate machines to be embedded as data in stores.
import { markRaw, shallowRef } from "vue";
import { createActor } from "xstate";
import { useStorage } from "@vueuse/core";

const inspect =
  process.env.NODE_ENV === "development" && import.meta.env.VITE_INSPECT_ACTORS === "true"
    ? (event) => console.log(event)
    : null;

const rehydrate = (machine) => {
  const cached = useStorage(machine.id).value;
  return cached === undefined || cached === "undefined" ? false : JSON.parse(cached);
};

export const useStoreMachine = (machine) => {
  const rehydrated = rehydrate(machine);
  const actor = createActor(machine, {
    inspect,
    snapshot: !rehydrated ? null : rehydrated.persistable,
  });

  actor.start();

  const state = shallowRef(actor.getSnapshot());
  const persistable = shallowRef(actor.getPersistedSnapshot());

  actor.subscribe((snapshot) => {
    state.value = snapshot;
    persistable.value = actor.getPersistedSnapshot();
  });

  return {
    actor: markRaw(actor),
    send: markRaw(actor.send),
    persistable,
    state,
  };
};

// Inline tests.
if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest;

  it("handles rehydration if there is no cached machine", () => {
    const rehydrated = rehydrate({ id: "someId" });
    expect(rehydrated).toBe(false);
  });

  it("handles rehydration if there is a string of 'undefined'", () => {
    window.localStorage.setItem("someId", "undefined");
    const rehydrated = rehydrate({ id: "someId" });
    expect(rehydrated).toBe(false);
  });

  it("handles rehydration if there is a cached machine", () => {
    const data = { some: "data" };
    window.localStorage.setItem("someId", JSON.stringify(data));
    const rehydrated = rehydrate({ id: "someId" });
    expect(rehydrated).toStrictEqual({ some: "data" });
  });
}
