const routes = [
  {
    path: "/",
    component: () => import("layouts/main/MainLayout.vue"),
    children: [
      {
        component: () => import("pages/dashboard/Dashboard"),
        name: "Dashboard",
        path: "",
        props: { icon: "dashboard" },
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
