import { createWebHistory, createRouter } from "vue-router";

import { API } from "@/api";
import { dbUrl } from "@/api/config";
import store from "@/store";

const history = createWebHistory("/ui/");

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: () => import("@/views/Dashboard"),
  },
];

const router = createRouter({ history, routes });

router.beforeEach(async (to, from, next) => {
  const { success, data } = await API.auth.session();
  if (success) {
    store.commit("addUser", data);
    next();
  } else {
    store.commit("deleteUser");
    window.location.href = dbUrl;
  }
});

export default router;
