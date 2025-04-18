// Test the stores/auth module.
import { createPinia, defineStore, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { createActor } from "xstate";

import { oAuthMachine } from "@/stores/auth";
import { useStoreMachine } from "@/use";

const VITE_OAUTH_CLIENT_ID = "oauth.ida.development";

describe("the auth store", () => {
  beforeEach(() => {
    vi.stubEnv("VITE_OAUTH_CLIENT_ID", VITE_OAUTH_CLIENT_ID);
    setActivePinia(createPinia());
  });

  it("initializes the auth store correctly for the PKCE flow", () => {
    const actor = createActor(oAuthMachine);
    actor.start();

    actor.subscribe((snapshot) => {
      expect(snapshot.value).toStrictEqual({ no: "authenticate" });
      expect(snapshot.context.clientId).toBe(VITE_OAUTH_CLIENT_ID);
      expect(snapshot.context.codeVerifier).not.toBeNull();
      expect(snapshot.context.codeChallenge).not.toBeNull();
    });
  });

  it("initializes the auth store correctly via xstore", () => {
    const useAuthStore = defineStore(oAuthMachine.id, () => useStoreMachine(oAuthMachine));
    const store = useAuthStore();

    store.actor.subscribe((snapshot) => {
      expect(snapshot.value).toStrictEqual({ no: "authenticate" });
      expect(snapshot.context.clientId).toBe(VITE_OAUTH_CLIENT_ID);
      expect(snapshot.context.codeVerifier).not.toBeNull();
      expect(snapshot.context.codeChallenge).not.toBeNull();
    });
  });
});
