import { ref } from "vue";
import { assign, createMachine } from "xstate";

import { fetcher } from "./config";

const fetchMachine = createMachine({
  id: fetcher,
  initial: "loading",
  context: {
    request: null,
    data: null,
    status: null,
    error: null,
    apiError: null,
    redirected: null,
    retries: 0,
    maxRetries: 3,
  },
  states: {
    loading: {
      invoke: {
        src: "fetch",
        onDone: {
          target: "success",
          actions: "setData",
        },
        onError: {
          target: "failure",
          actions: "setError",
        },
      },
    },
    failure: {
      on: {
        RETRY: {
          always: [
            { target: "loading", cond: "canRetry" },
            { target: "fatal" },
          ],
          actions: "incrementRetries",
        },
      },
    },
    success: {
      target: "final",
    },
    fatal: {
      target: "final",
    },
    reauthenticate: {
      target: "final",
    },
  },
  actions: {
    incrementRetries: assign({
      retries: (context) => context.retries + 1,
    }),
    setData: assign({
      data: (_, event) => event.data,
      status: (_, event) => event.status,
      redirected: (_, event) => event.redirected,
    }),
    setError: assign({
      error: (_, event) => event.data,
      apiError: (_, event) => event.error,
      status: (_, event) => event.status,
      redirected: (_, event) => event.redirected,
    }),
  },
  guards: {
    canRetry: ({ retries, maxRetries }) => retries < maxRetries,
    // TODO: Need to integrate reauth logic here.
  },
  services: {
    fetch: (context) => {
      return fetch(context.request, { credentials: "include" }).then(
        (response) => response.json(),
      );
    },
  },
});

// const fetchAPI = (request) => {
//   const machine = useMachine(fetchMachine, { context: { request } });
//   const data = computed(() => machine.value.context.data);
//   const error = computed(() => machine.value.context.error);
//   const apiError = computed(() => machine.value.context.apiError);
//   const loading = computed(
//     () => !["success", "fatal"].some(machine.value.matches),
//   );
//   return {
//     apiError,
//     data,
//     error,
//     loading,
//     machine,
//   };
// };

const API = (context = null) => {
  const loading = ref(false);
  const success = ref(null);
  const status = ref(null);
  const data = ref(null);
  const apiError = ref(null);
  const redirected = ref(null);
  const error = ref(false);

  const fetchAPI = (request) => {
    loading.value = true;
    error.value = undefined;

    return fetcher(request)
      .then(async (response) => {
        success.value = response.ok;
        status.value = response.status;
        redirected.value = response.redirected || false;
        apiError.value = response.error || false;
        data.value = await response.json();
        if (context) {
          context.emit("onReauthenticate", status.value === 403);
        }
      })
      .catch((e) => {
        error.value = e;
      });
  };

  return {
    apiError,
    data,
    error,
    fetchAPI,
    loading,
    redirected,
    status,
    success,
  };
};

export default API;
