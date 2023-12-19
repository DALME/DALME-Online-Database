// Test the stores/auth module.
import { oAuthMachine } from "@/stores/auth";
import { createPinia, defineStore, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { createActor } from "xstate";

import { useStoreMachine } from "@/use";

const OAUTH_CLIENT_ID = "oauth.ida.development";

describe("the auth store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  vi.stubEnv("VITE_OAUTH_CLIENT_ID", OAUTH_CLIENT_ID);

  it("initializes the auth store correctly for the PKCE flow", () => {
    const actor = createActor(oAuthMachine);
    actor.start();

    actor.subscribe((snapshot) => {
      expect(snapshot.value).toStrictEqual({ no: "authenticate" });
      expect(snapshot.context.clientId).toBe(OAUTH_CLIENT_ID);
      expect(snapshot.context.codeVerifier).not.toBeNull();
      expect(snapshot.context.codeChallenge).not.toBeNull();
    });
  });

  it("initializes the auth store correctly via xstore", () => {
    const useAuthStore = defineStore(oAuthMachine.id, () => useStoreMachine(oAuthMachine));
    const store = useAuthStore();

    store.actor.subscribe((snapshot) => {
      expect(snapshot.value).toStrictEqual({ no: "authenticate" });
      expect(snapshot.context.clientId).toBe(OAUTH_CLIENT_ID);
      expect(snapshot.context.codeVerifier).not.toBeNull();
      expect(snapshot.context.codeChallenge).not.toBeNull();
    });
  });
});
