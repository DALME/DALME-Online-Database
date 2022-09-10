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
            props: { icon: "home_work" },
            nav: true,
            meta: {
              sourceType: "archives",
              sourceTypeAPI: "archives",
            },
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Archival Files",
            path: "archival-files",
            props: { icon: "inventory" },
            nav: true,
            meta: {
              sourceType: "archivalFiles",
              sourceTypeAPI: "archival_files",
            },
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Records",
            path: "records",
            props: { icon: "text_snippet" },
            nav: true,
            meta: {
              sourceType: "records",
              sourceTypeAPI: "records",
            },
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Bibliography",
            path: "bibilographies",
            props: { icon: "local_library" },
            nav: true,
            meta: {
              sourceType: "bibliography",
              sourceTypeAPI: "bibliography",
            },
          },
        ],
      },

      {
        // Sets
        component: () => import("pages/set-root/SetRoot.vue"),
        name: "Sets",
        path: "sets",
        props: { icon: "folder_copy" },
        nav: true,
        redirect: "/sets/datasets",
        children: [
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Corpora",
            path: "corpora",
            props: { icon: "drive_folder_upload" },
            nav: true,
            meta: {
              setType: "corpora",
              setTypeAPI: "corpora",
            },
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Collections",
            path: "collections",
            props: { icon: "folder_special" },
            nav: true,
            meta: {
              setType: "collections",
              setTypeAPI: "collections",
            },
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Datasets",
            path: "datasets",
            props: { icon: "topic" },
            nav: true,
            meta: {
              setType: "datasets",
              setTypeAPI: "datasets",
            },
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Worksets",
            path: "worksets",
            props: { icon: "rule_folder" },
            nav: true,
            meta: {
              setType: "worksets",
              setTypeAPI: "worksets",
            },
          },
        ],
      },

      {
        // Entities
        component: () => import("pages/entity-root/EntityRoot.vue"),
        name: "Entities",
        path: "entities",
        props: { icon: "api" },
        nav: true,
        redirect: "/entities/agents",
        children: [
          {
            component: () => import("pages/agent-list/AgentList.vue"),
            name: "Agents",
            path: "agents",
            props: { icon: "groups" },
            nav: true,
          },
          {
            component: () => import("pages/place-list/PlaceList.vue"),
            name: "Places",
            path: "places",
            props: { icon: "place" },
            nav: true,
          },
        ],
      },

      {
        // Project
        component: () => import("pages/project-root/ProjectRoot.vue"),
        name: "Project",
        path: "project",
        props: { icon: "business_center" },
        nav: true,
        redirect: "/project/tasks",
        children: [
          {
            component: () => import("pages/task-list/TaskList.vue"),
            name: "Tasks",
            path: "tasks",
            props: { icon: "checklist" },
            nav: true,
          },
          {
            component: () => import("pages/ticket-list/TicketList.vue"),
            name: "Tickets",
            path: "tickets",
            props: { icon: "bug_report" },
            nav: true,
          },
          {
            component: () => import("pages/library-list/LibraryList.vue"),
            name: "Library",
            path: "library",
            props: { icon: "menu_book" },
            nav: true,
          },
          {
            component: () => import("pages/rights-list/RightsList.vue"),
            name: "Rights Policies",
            path: "rights",
            props: { icon: "copyright" },
            nav: true,
          },
        ],
      },

      {
        // System
        component: () => import("pages/system-root/SystemRoot.vue"),
        name: "System",
        path: "system",
        props: { icon: "display_settings" },
        nav: true,
        redirect: "/system/locales",
        children: [
          {
            component: () => import("pages/locale-list/LocaleList.vue"),
            name: "Locales",
            path: "locales",
            props: { icon: "location_city" },
            nav: true,
          },
          {
            component: () => import("pages/country-list/CountryList.vue"),
            name: "Countries",
            path: "countries",
            props: { icon: "flag" },
            nav: true,
          },
          {
            component: () => import("pages/language-list/LanguageList.vue"),
            name: "Languages",
            path: "languages",
            props: { icon: "translate" },
            nav: true,
          },
          {
            component: () => import("pages/user-list/UserList.vue"),
            name: "Users",
            path: "users",
            props: { icon: "supervisor_account" },
            nav: true,
          },
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

      /* Detail Views */
      // TODO: Need to properly scope these...
      {
        component: () => import("pages/rights/Rights.vue"),
        name: "Rights",
        path: "rights/:id",
        props: true,
        nav: false,
        meta: {
          navPath: ["Project", "Rights Policies"],
        },
      },
      {
        component: () => import("pages/set/Set.vue"),
        name: "Set",
        path: "sets/:id",
        nav: false,
        meta: {
          navPath: ["Sets"],
        },
      },
      {
        component: () => import("pages/source/Source.vue"),
        name: "Source",
        path: "sources/:id",
        nav: false,
        meta: {
          navPath: ["Sources"],
        },
      },
      {
        component: () => import("pages/task/Task.vue"),
        name: "Task",
        path: "tasks/:id",
        nav: false,
        meta: {
          navPath: ["Project", "Tasks"],
        },
      },
      {
        component: () => import("pages/ticket/Ticket.vue"),
        name: "Ticket",
        path: "tickets/:id",
        nav: false,
        meta: {
          navPath: ["Project", "Tickets"],
        },
      },
      {
        component: () => import("pages/user/User.vue"),
        name: "User",
        path: "system/users/:username",
        nav: false,
        meta: {
          navPath: ["System", "Users"],
        },
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
