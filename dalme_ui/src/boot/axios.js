import { boot } from "quasar/wrappers";
import axios from "axios";
import { tokenRefreshUrl } from "../api/config";
import { useAuthStore } from "stores/auth";

const fetcher = axios.create();
fetcher.defaults.headers.post["Content-Type"] = "application/json";

export default boot(({ store }) => {
  fetcher.interceptors.response.use(
    // status code in the 2xx range
    (response) => {
      return response;
    },
    // status code outside the 2xx range
    async (error) => {
      const authStore = useAuthStore(store);
      const originalConfig = error.config;

      if (error.response.status === 401 && !originalConfig._isRetry) {
        try {
          originalConfig._isRetry = true;
          const retryRequest = new Promise((resolve) => {
            authStore.requestQueue.push(() => {
              resolve(fetcher(originalConfig));
            });
          });

          if (!authStore.isRefreshing) {
            authStore.isRefreshing = true;
            const refresh = await axios.post(tokenRefreshUrl);
            if (!refresh.status === 200) {
              authStore.reAuthenticate = true;
            }
            authStore.isRefreshing = false;
            authStore.processQueue();
          }

          return retryRequest;
        } catch (refreshError) {
          authStore.reAuthenticate = true;
          return Promise.reject(refreshError);
        }
      } else {
        return Promise.reject(error);
      }
    },
  );
});

export { fetcher };
