const routes = [
  {
    path: "/",
    component: () => import("layouts/main/MainLayout.vue"),
    children: [
      {
        component: () => import("pages/dashboard/Dashboard.vue"),
        name: "Dashboard",
        path: "",
        props: { icon: "dashboard" },
        nav: true,
      },
      {
        component: () => import("pages/source-root/SourceRoot.vue"),
        name: "Sources",
        path: "sources",
        props: { icon: "bookmark" },
        nav: true,
        redirect: "/sources/records",
        children: [
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Archives",
            path: "archives",
            nav: true,
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Archival Files",
            path: "archival-files",
            nav: true,
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Records",
            path: "records",
            nav: true,
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Bibliographies",
            path: "bibilographies",
            nav: true,
          },
        ],
      },
      {
        component: () => import("pages/task-list/TaskList.vue"),
        name: "Tasks",
        path: "tasks",
        props: { icon: "assignment" },
        nav: true,
      },
      {
        component: () => import("pages/task/Task.vue"),
        name: "Task",
        path: "tasks/:objId",
        props: true,
        nav: false,
      },
      {
        component: () => import("pages/ticket-list/TicketList.vue"),
        name: "Tickets",
        path: "tickets",
        props: { icon: "subject" },
        nav: true,
      },
      {
        component: () => import("pages/ticket/Ticket.vue"),
        name: "Ticket",
        path: "tickets/:objId",
        props: true,
        nav: false,
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
