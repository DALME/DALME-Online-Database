import { createPinia } from "pinia";
import { createORM } from "pinia-orm";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
pinia.use(
  createORM({
    pinia: {
      storeType: "setupStore",
    },
    model: {
      withMeta: true,
      hidden: [],
    },
  }),
);
export default pinia;
