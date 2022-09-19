import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";

import { filter as rFilter, head } from "ramda";
import routes from "./routes";
import { useNavStore } from "@/stores/navigation";

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

export const navRoutes = rFilter(
  (route) => route.nav,
  head(router.options.routes).children,
);

const navSections = navRoutes.map((value) => {
  return value.name;
});

const navSubsections = rFilter((route) => route.children, navRoutes)
  .reduce(
    (previousValue, currentValue) => [
      ...previousValue,
      ...currentValue.children,
    ],
    [],
  )
  .map((value) => {
    return value.name;
  });

router.beforeEach((to, from) => {
  const $navStore = useNavStore();
  const navSection = navSections.includes(to.matched[1].name)
    ? to.matched[1].name
    : null;
  const navSubsection =
    to.matched.length > 2 && navSubsections.includes(to.matched[2].name)
      ? to.matched[2].name
      : null;
  const navPathLen = to.meta.navPath ? to.meta.navPath.length : 0;
  const navPathSection = navPathLen > 0 ? to.meta.navPath[0] : "";
  const navPathSubsection = navPathLen > 1 ? to.meta.navPath[1] : "";
  const currentSection = navSection || navPathSection;
  let currentSubsection = navSubsection || navPathSubsection;

  if (
    from.matched.length > 2 &&
    from.matched[1].name == currentSection &&
    to.matched.length < 3
  ) {
    currentSubsection = from.matched[2].name;
  }

  $navStore.currentSection = currentSection;
  $navStore.currentSubsection = currentSubsection;
});

export default router;
