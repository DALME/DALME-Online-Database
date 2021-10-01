import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";

import { API as useAPI, loginUrl, requests } from "@/api";
import { sessionSchema } from "@/schemas";
import store from "@/store";

import routes from "./routes";

const createHistory = process.env.SERVER
  ? createMemoryHistory
  : process.env.VUE_ROUTER_MODE === "history"
    ? createWebHistory  // prettier-ignore
    : createWebHashHistory; // prettier-ignore

export const router = createRouter({
  routes,
  history: createHistory(
    process.env.MODE === "ssr" ? void 0 : process.env.VUE_ROUTER_BASE,
  ),
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

router.beforeEach(async (to) => {
  const { data, fetchAPI, success } = useAPI();
  await fetchAPI(requests.auth.session());
  if (success.value) {
    await sessionSchema.validate(data.value).then((value) => {
      store.dispatch("auth/login", value);
    });
  } else {
    await store.dispatch("auth/logout");
    window.location.href = `${loginUrl}?next=${to.href}`;
  }
});

export default router;
