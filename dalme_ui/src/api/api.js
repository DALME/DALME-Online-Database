import { isNil } from "ramda";
import { ref } from "vue";

import { fetcher } from "./config";

const API = (reauthenticate = null) => {
  const loading = ref(true);
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
        data.value = await response.json();
        success.value = response.ok;
        status.value = response.status;
        redirected.value = response.redirected || false;
        apiError.value = response.error || false;
        if (!isNil(reauthenticate)) {
          if (response.status === 200) reauthenticate(false);
          if (response.status === 201) reauthenticate(false);
          if (response.status === 403) reauthenticate(true);
        }
      })
      .catch((e) => {
        error.value = e;
        // TODO: Show internal error.
      })
      .finally(() => (loading.value = false));
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
