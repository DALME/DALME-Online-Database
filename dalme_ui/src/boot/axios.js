// Initialize the axios fetcher.
import axios from "axios";
import { boot } from "quasar/wrappers";
import { isNil } from "ramda";

import { useAuthStore } from "stores/auth";

const fetcher = axios.create();

fetcher.defaults.xsrfCookieName = "csrftoken";
fetcher.defaults.xsrfHeaderName = "X-CSRFToken";
fetcher.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";

export default boot(({ store }) => {
  fetcher.interceptors.request.use(
    (config) => {
      const { accessToken } = useAuthStore();
      if (!isNil(accessToken)) {
        config.headers["Authorization"] = `Bearer ${accessToken}`;
      }
      return config;
    },
    (error) => {
      Promise.reject(error);
    },
  );
  fetcher.interceptors.response.use(
    // Status code in the 2xx range.
    (response) => {
      return response;
    },

    // Status code outside the 2xx range.
    async (error) => {
      const auth = useAuthStore(store);

      if (error.response.status === 401) {
        return new Promise((resolve) => {
          auth.queue.push(() => resolve(fetcher(error.config)));
          auth.send({ type: "REFRESH" });
        });
      } else {
        return Promise.reject(error);
      }
    },
  );
});

export { fetcher };
