import { createWebHistory, createRouter } from "vue-router";

import { API as useAPI, loginUrl, requests } from "@/api";
import store from "@/store";

const history = createWebHistory("/ui/");

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: () => import("@/views/Dashboard"),
  },
  {
    path: "/search",
    name: "search",
    component: () => import("@/views/Search"),
  },
];

const router = createRouter({ history, routes });

router.beforeEach(async (to, from, next) => {
  const { data, fetchAPI, success } = useAPI();
  await fetchAPI(requests.auth.session());
  if (success.value) {
    store.commit("addUser", data.value);
    next();
  } else {
    store.commit("deleteUser");
    window.location.href = `${loginUrl}?next=${to.href}`;
  }
});

export default router;
