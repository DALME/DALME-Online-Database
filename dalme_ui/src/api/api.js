import { ref } from "vue";

import { fetcher } from "./config";

const API = (reauthenticate) => {
  const loading = ref(false);
  const success = ref(null);
  const status = ref(null);
  const data = ref(null);
  const apiError = ref(null);
  const redirected = ref(null);
  const error = ref(false);

  const fetchAPI = (request) => {
    loading.value = true;
    error.value = false;

    return fetcher(request)
      .then(async (response) => {
        success.value = response.ok;
        status.value = response.status;
        redirected.value = response.redirected || false;
        apiError.value = response.error || false;
        data.value = await response.json();
        reauthenticate.value = status.value === 403;
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
