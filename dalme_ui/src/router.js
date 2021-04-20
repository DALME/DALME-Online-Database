import { createWebHistory, createRouter } from "vue-router";

const history = createWebHistory("/ui/");

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: () => import("@/views/Dashboard"),
  },
];

const router = createRouter({ history, routes });

export default router;
