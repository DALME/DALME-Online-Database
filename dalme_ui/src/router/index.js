import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import { head, isEmpty } from "ramda";
import routes from "./routes";
import { useNavStore } from "@/stores/navigation";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";
// import { provideErrorHandling } from "@/use";

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

export const navRoutes = head(router.options.routes).children;

router.beforeEach((_, from) => {
  const views = useViewStore();
  if (
    from &&
    !isEmpty(from.meta) &&
    !from.meta.resetStateOnLoad &&
    !isEmpty(views.view)
  ) {
    views.saveViewState(from.fullPath);
  }
});

router.beforeResolve(async (to) => {
  const nav = useNavStore();
  const ui = useUiStore();
  const views = useViewStore();
  await nav.setPageState(to);
  ui.setUiState(to);
  views.setViewState(to);
});

export default router;
