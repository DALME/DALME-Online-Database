// Define the auth store machine interface.
import { encode as base64encode } from "base64-arraybuffer";
import * as changeKeys from "change-case/keys";
import cryptoRandomString from "crypto-random-string";
import { defineStore } from "pinia";
import { Notify } from "quasar";
import { has, isNil } from "ramda";
import { computed, ref, watch } from "vue";
import { assign, fromCallback, fromPromise, setup } from "xstate";
import { useSelector } from "@xstate/vue";
import * as yup from "yup";

import { API as apiInterface, requests } from "@/api";
import { router as $router } from "@/router";
import { groupSchema, tenantSchema } from "@/schemas";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";
import { useStoreMachine } from "@/use";

const AUTHORIZATION_CALLBACK_URL = "api/oauth/authorize/callback/";
const CODE_CHALLENGE_METHOD = "S256";
const CODE_VERIFIER_LENGTH = 128;
const RESPONSE_TYPE = "code";

const userInfoSchema = yup
  .object()
  .shape({
    userId: yup.number().required(),
    username: yup.string().required(),
    fullName: yup.string().nullable(),
    email: yup.string().email().required(),
    avatar: yup.string().default(null).nullable(),
    isAdmin: yup.boolean().required(),
    groups: yup.array().of(groupSchema).default(null).nullable(),
    tenant: tenantSchema,
  })
  .camelCase()
  .transform((data) => {
    return {
      ...data,
      userId: data.sub,
    };
  });

// To protect against vulnerabilities we don't keep the access token in the
// machine context as it would then be persisted in localstorage. Instead we
// just keep it in app memory lasting the duration of the tab/window lifetime.
// Then, when the machine is rehydrated, if the app finds itself in the
// 'yes.authorized' state but without an accessToken ready-to-hand, it can
// request a new access token using the long duration refresh token which is
// stored safely in an HTTP only cookie.
const accessToken = ref(null);

// Define utilities.
const getClientId = () => import.meta.env.VITE_OAUTH_CLIENT_ID;

const getCodeVerifier = () => cryptoRandomString({ length: CODE_VERIFIER_LENGTH });

const getCodeChallenge = async (codeVerifier) => {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await window.crypto.subtle.digest("SHA-256", data);
  const base64digest = base64encode(digest);
  return base64digest.replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
};

const getRedirectURI = () => `${window.location.origin}/${AUTHORIZATION_CALLBACK_URL}`;

const setCSRFToken = async () => {
  const { fetchAPI } = apiInterface();
  await fetchAPI(requests.auth.CSRF());
};

// Define actor actions.
const checkTokens = fromCallback(({ input, sendBack }) => {
  if (isNil(accessToken.value) && !isNil(input.idToken)) {
    sendBack({ type: "REFRESH" });
  }
});

const fetchAuthorization = fromPromise(async ({ input: { clientId, codeChallenge } }) => {
  const body = {
    clientId,
    codeChallenge,
    responseType: RESPONSE_TYPE,
    codeChallengeMethod: CODE_CHALLENGE_METHOD,
    redirectUri: getRedirectURI(),
  };
  const params = new URLSearchParams(changeKeys.snakeCase(body));
  const { fetchAPI, responseURL, success } = apiInterface();
  await fetchAPI(requests.auth.authorize(params));

  if (success.value) {
    const url = new URL(responseURL.value);
    return url.searchParams.get("code");
  } else {
    throw new Error("Failed to authorize");
  }
});

const fetchTokens = fromPromise(
  async ({ input: { authorizationCode, clientId, codeVerifier } }) => {
    const body = {
      clientId,
      codeVerifier,
      code: authorizationCode,
      grantType: "authorization_code",
      redirectUri: getRedirectURI(),
      scope: "openid",
    };
    const params = new URLSearchParams(changeKeys.snakeCase(body));
    const { data, fetchAPI, success } = apiInterface();
    await fetchAPI(requests.auth.token(params));

    if (success.value) {
      const payload = changeKeys.camelCase(data.value);
      accessToken.value = payload.accessToken;
      delete payload.accessToken;
      return payload;
    } else {
      throw new Error("Unable to retrieve OAuth credentials");
    }
  },
);

const fetchUser = fromPromise(async () => {
  const { data, fetchAPI, success } = apiInterface();
  await fetchAPI(requests.auth.authUser());

  if (success.value) {
    await userInfoSchema.validate(data.value).then((value) => {
      data.value = value;
    });
    return data.value;
  } else {
    throw new Error("Unable to fetch user data");
  }
});

const fetchRefresh = fromCallback(({ input: { clientId }, sendBack }) => {
  const body = {
    clientId,
    grantType: "refresh_token",
  };
  const params = new URLSearchParams(changeKeys.snakeCase(body));
  const { data, fetchAPI } = apiInterface();

  fetchAPI(requests.auth.token(params))
    .then(() => {
      const payload = changeKeys.camelCase(data.value);
      accessToken.value = payload.accessToken;
      sendBack({ type: "REFRESHED" });
    })
    .error(() => {
      sendBack({ type: "FAILED", error: { message: "Unable to refresh token" } });
    });
});

const fetchLogout = fromPromise(async ({ input: { idToken } }) => {
  const body = { idTokenHint: idToken };
  const params = new URLSearchParams(changeKeys.snakeCase(body));
  const { fetchAPI, success } = apiInterface();
  await fetchAPI(requests.auth.logout(params));

  if (!success.value) {
    throw new Error("Unable to logout");
  }
});

const generateChallenge = fromPromise(async () => {
  const codeVerifier = getCodeVerifier();
  const codeChallenge = await getCodeChallenge(codeVerifier);
  return {
    codeVerifier,
    codeChallenge,
  };
});

const logoutReset = () => {
  accessToken.value = null;
};

const redirect500 = () => {
  $router.push({ name: "HTTP 500" });
};

// Define machines

// PKCE/OIDC authentication flow machine.
const pkceFlow = {
  id: "no",
  initial: "mode",
  invoke: {
    src: "generateChallenge",
    onDone: {
      actions: assign({
        clientId: () => getClientId(),
        codeVerifier: ({ event }) => event.output.codeVerifier,
        codeChallenge: ({ event }) => event.output.codeChallenge,
        error: () => null,
      }),
    },
    onError: {
      target: "fatal",
      actions: assign({ error: ({ event }) => event.error.message }),
    },
  },
  states: {
    mode: {
      always: [
        {
          guard: ({ context }) => !isNil(context.idToken),
          target: "reauthenticate",
        },
        {
          target: "authenticate",
        },
      ],
    },
    authenticate: {
      on: {
        LOGIN: {
          target: "authorize",
        },
        LOGIN_FAILED: {
          target: "#no",
        },
      },
    },
    reauthenticate: {
      on: {
        LOGIN: {
          target: "authorize",
        },
        LOGIN_FAILED: {
          target: "#no",
        },
      },
    },
    authorize: {
      invoke: {
        src: "fetchAuthorization",
        input: ({ context }) => ({
          clientId: context.clientId,
          codeChallenge: context.codeChallenge,
        }),
        onDone: {
          target: "tokenize",
          actions: assign({ authorizationCode: ({ event }) => event.output }),
        },
        onError: {
          target: "#no",
          actions: assign({ error: ({ event }) => event.error.message }),
        },
      },
    },
    tokenize: {
      invoke: {
        src: "fetchTokens",
        input: ({ context }) => ({
          authorizationCode: context.authorizationCode,
          clientId: context.clientId,
          codeVerifier: context.codeVerifier,
        }),
        onDone: {
          target: "#yes",
          actions: [
            assign({
              authorizationCode: () => null,
              idToken: ({ event }) => event.output.idToken,
            }),
          ],
        },
        onError: {
          target: "#no",
          actions: assign({ error: ({ event }) => event.error.message }),
        },
      },
    },
  },
};

// Authorization code flow machine.
const authFlow = {
  id: "yes",
  initial: "authorized",
  invoke: {
    id: "getUserData",
    src: "fetchUser",
    onDone: {
      target: "yes.authorized",
      actions: assign({ user: ({ event }) => event.output }),
    },
    onError: {
      target: "#no",
      actions: assign({ error: ({ event }) => event.error.message }),
    },
  },
  states: {
    authorized: {
      invoke: {
        src: "checkTokens",
        input: ({ context }) => ({ idToken: context.idToken }),
      },
      on: {
        EXPIRE: {
          target: "expire",
        },
        LOGOUT: {
          target: "logout",
        },
        REFRESH: {
          target: "refresh",
        },
      },
    },
    refresh: {
      invoke: {
        src: "fetchRefresh",
        input: ({ context }) => ({ clientId: context.clientId }),
      },
      on: {
        REFRESHED: {
          target: "authorized",
        },
        FAILED: {
          target: "expire",
          actions: assign({ error: ({ event }) => event.error.message }),
        },
      },
    },
    expire: {
      invoke: {
        src: "fetchLogout",
        input: ({ context }) => ({ idToken: context.idToken }),
        onDone: {
          target: "#no.reauthenticate",
          actions: [
            "logoutReset",
            assign({
              clientId: () => null,
              error: () => null,
              idToken: () => null,
              scope: () => null,
              user: () => null,
            }),
          ],
        },
        onError: {
          target: "authorized",
          actions: assign({ error: ({ event }) => event.error.message }),
        },
      },
    },
    logout: {
      invoke: {
        src: "fetchLogout",
        input: ({ context }) => ({ idToken: context.idToken }),
        onDone: {
          target: "#no.authenticate",
          actions: [
            "logoutReset",
            assign({
              clientId: () => null,
              error: () => null,
              idToken: () => null,
              scope: () => null,
              user: () => null,
            }),
          ],
        },
        onError: {
          target: "authorized",
          actions: assign({ error: ({ event }) => event.error.message }),
        },
      },
    },
  },
};

// OAuth 2.0 with PKCE enchancement machine.
export const oAuthMachine = setup({
  actions: {
    logoutReset,
    redirect500,
  },
  actors: {
    checkTokens,
    fetchAuthorization,
    fetchLogout,
    fetchRefresh,
    fetchTokens,
    fetchUser,
    generateChallenge,
  },
}).createMachine({
  id: "oauth",
  initial: "no",
  context: {
    authorizationCode: null,
    clientId: null,
    codeChallenge: null,
    codeVerifier: null,
    error: null,
    idToken: null,
    scope: null,
    user: null,
  },
  states: {
    no: pkceFlow,
    yes: authFlow,
    fatal: {
      entry: ["redirect500"],
    },
  },
});

export const useAuthStore = defineStore(
  oAuthMachine.id,
  () => {
    const { actor, persistable, send, state } = useStoreMachine(oAuthMachine);

    const user = useSelector(actor, ({ context: { user } }) => user);
    const error = useSelector(actor, ({ context: { error } }) => error);

    const currentState = computed(() => state.value.value);
    const authorized = computed(() => has("yes")(currentState.value) && !isNil(user.value));
    const unauthorized = computed(() => !authorized.value);
    const authenticate = computed(
      () => unauthorized.value && currentState.value.no === "authenticate",
    );
    const reauthenticate = computed(
      () => unauthorized.value && currentState.value.no === "reauthenticate",
    );

    const queue = ref([]);
    const processQueue = async () => {
      await queue.value.forEach((callback) => callback());
      queue.value = [];
    };

    const logout = () => {
      actor.send({ type: "LOGOUT" });
      ui.$reset();
      views.$reset();
    };

    watch(
      () => currentState.value,
      (oldState, newState) => {
        const refreshed = () => oldState.yes === "refresh" && newState.yes === "authorized";
        if (authorized.value && refreshed()) {
          processQueue();
        }
      },
    );

    watch(
      () => error.value,
      (newValue) => {
        if (!isNil(newValue)) {
          Notify.create({
            color: "red",
            message: newValue,
            position: "top-right",
            icon: "speaker_notes",
          });
        }
      },
    );

    // TODO: Decomplect these.
    const ui = useUiStore();
    const views = useViewStore();

    return {
      accessToken,
      actor,
      authenticate,
      authorized,
      logout,
      persistable,
      reauthenticate,
      send,
      setCSRFToken,
      state,
      unauthorized,
      user,
      // TODO: Refresh sub flow/machine?
      processQueue,
      queue,
    };
  },
  {
    persist: { paths: ["persistable"] },
  },
);

// Inline tests.
if (import.meta.vitest) {
  const { it, expect, vi } = import.meta.vitest;

  vi.stubEnv("VITE_OAUTH_CLIENT_ID", "oauth.ida.development");

  it("reads the OAUTH_CLIENT_ID from the environment", () => {
    expect(getClientId()).toBe("oauth.ida.development");
  });

  it("generates a random code verifier of a given length", () => {
    const value = getCodeVerifier();
    expect(value.length).toBe(CODE_VERIFIER_LENGTH);
  });

  it("generates a code challenge from a code verifier", async () => {
    const codeVerifier = "some-random-code-verifier";
    const value = await getCodeChallenge(codeVerifier);
    expect(value).toBe("Vu-F4aVqACp3hX7guN0m-fwYkIiVNUGPgev5hraCRBk");
  });

  it("reads the OAuth redirect uri", () => {
    const value = getRedirectURI();
    expect(value).toBe("http://localhost:3000/api/oauth/authorize/callback/");
  });
}
