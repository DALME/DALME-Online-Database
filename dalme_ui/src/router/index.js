import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import { head, isEmpty, filter as rFilter } from "ramda";
import routes from "./routes";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";
import Cookies from "js-cookie";
import { isNil } from "ramda";

const createHistory = process.env.SERVER
  ? createMemoryHistory
  : process.env.VUE_ROUTER_MODE === "history"
    ? createWebHistory  // prettier-ignore
    : createWebHashHistory; // prettier-ignore

export const router = createRouter({
  routes,
  history: createHistory(process.env.MODE === "ssr" ? void 0 : process.env.VUE_ROUTER_BASE),
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

router.beforeEach((_, from) => {
  const auth = useAuthStore();
  if (isNil(Cookies.get("csrftoken"))) {
    auth.setCSRFToken();
  }
  const views = useViewStore();
  if (from && !isEmpty(from.meta) && !from.meta.resetStateOnLoad && !isEmpty(views.view)) {
    views.saveViewState(from.fullPath);
  }
});

router.beforeResolve(async (to) => {
  const ui = useUiStore();
  const views = useViewStore();
  await ui.setPageState(to);
  ui.setUiState(to);
  views.setViewState(to);
});

export default router;
