import Cookies from "js-cookie";
import { head, isNil, filter as rFilter } from "ramda";
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from "vue-router";

import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";

import routes from "./routes";

const createHistory = process.env.SERVER
  ? createMemoryHistory
  : process.env.VUE_ROUTER_MODE === "history"
    ? createWebHistory  // prettier-ignore
    : createWebHashHistory; // prettier-ignore

export const router = createRouter({
  routes,
  history: createHistory(process.env.VUE_ROUTER_BASE),
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

export const navRoutes = (menu = null) => {
  const routes = head(router.options.routes).children;
  if (menu == null) {
    return routes;
  } else {
    return rFilter((r) => r.menu == menu, routes);
  }
};

router.beforeEach(() => {
  const auth = useAuthStore();
  if (isNil(Cookies.get("csrftoken"))) {
    auth.setCSRFToken();
  }
});

router.beforeResolve(async (to) => {
  console.log("router.beforeResolve");
  const ui = useUiStore();
  await ui.setPageState(to);
  ui.setUiState(to);
});

export default router;
