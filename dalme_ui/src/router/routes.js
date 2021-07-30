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

      /* Sections */
      {
        // Sources
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
            props: { icon: "villa" },
            nav: true,
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Archival Files",
            path: "archival-files",
            props: { icon: "inventory" },
            nav: true,
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Records",
            path: "records",
            props: { icon: "format_list_numbered" },
            nav: true,
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Bibliography",
            path: "bibilography",
            props: { icon: "library_books" },
            nav: true,
          },
        ],
      },

      {
        // Project
        component: () => import("pages/project-root/ProjectRoot.vue"),
        name: "Project",
        path: "project",
        props: { icon: "work" },
        nav: true,
        redirect: "/project/tasks",
        children: [
          {
            component: () => import("pages/task-list/TaskList.vue"),
            name: "Tasks",
            path: "tasks",
            props: { icon: "assignment" },
            nav: true,
          },
          {
            component: () => import("pages/ticket-list/TicketList.vue"),
            name: "Tickets",
            path: "tickets",
            props: { icon: "subject" },
            nav: true,
          },
        ],
      },

      {
        // System
        component: () => import("pages/system-root/SystemRoot.vue"),
        name: "System",
        path: "system",
        props: { icon: "settings" },
        nav: true,
        redirect: "/system/admin",
        children: [
          {
            component: {},
            name: "Admin",
            path: "admin",
            props: { icon: "admin_panel_settings" },
            nav: true,
            beforeEnter(_) {
              window.location.replace("/admin");
            },
          },
        ],
      },

      {
        // Sets
        component: () => import("pages/set-root/SetRoot.vue"),
        name: "Sets",
        path: "sets",
        props: { icon: "collections" },
        nav: true,
        redirect: "/sets/datasets",
        children: [
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Datasets",
            path: "datasets",
            props: { icon: "snippet_folder" },
            nav: true,
          },
        ],
      },

      /* Detail Views */
      // TODO: Scope paths by section?
      {
        component: () => import("pages/language/Language.vue"),
        name: "Language",
        path: "languages/:objId",
        props: true,
        nav: false,
      },
      {
        component: () => import("pages/locale/Locale.vue"),
        name: "Locale",
        path: "locales/:objId",
        props: true,
        nav: false,
      },
      {
        component: () => import("pages/rights/Rights.vue"),
        name: "Rights",
        path: "rights/:objId",
        props: true,
        nav: false,
      },
      {
        component: () => import("pages/set/Set.vue"),
        name: "Set",
        path: "set/:objId",
        props: true,
        nav: false,
      },
      {
        component: () => import("pages/source/Source.vue"),
        name: "Source",
        path: "sources/:objId",
        props: true,
        nav: false,
      },
      {
        component: () => import("pages/task/Task.vue"),
        name: "Task",
        path: "tasks/:objId",
        props: true,
        nav: false,
      },
      {
        component: () => import("pages/ticket/Ticket.vue"),
        name: "Ticket",
        path: "tickets/:objId",
        props: true,
        nav: false,
      },
      {
        component: () => import("pages/user/User.vue"),
        name: "User",
        path: "users/:username",
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
