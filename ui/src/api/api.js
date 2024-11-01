import { ref } from "vue";
import { fetcher } from "../boot/axios";

const API = () => {
  const loading = ref(false);
  const success = ref(null);
  const status = ref(null);
  const data = ref(null);
  const apiError = ref(null);
  const redirected = ref(null);
  const error = ref(false);
  const responseURL = ref(null);

  const fetchAPI = (request) => {
    loading.value = true;
    error.value = false;

    return fetcher(request)
      .then((response) => {
        success.value = response.status >= 200 && response.status <= 299;
        status.value = response.status;
        // redirected.value = response.request.res.responseUrl === response.config.url;
        redirected.value = false;
        apiError.value = !success.value;
        data.value = response.data;
        responseURL.value = response.request.responseURL;
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
    responseURL,
    status,
    success,
  };
};

export default API;
