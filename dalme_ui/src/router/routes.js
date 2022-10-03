const routes = [
  {
    path: "/",
    component: () => import("layouts/main/MainLayout.vue"),
    children: [
      {
        component: () => import("pages/dashboard/Dashboard.vue"),
        name: "Dashboard",
        path: "",
        meta: { icon: "o_space_dashboard" },
        nav: true,
      },

      /* Sections */
      {
        // Sources
        component: () => import("pages/source-root/SourceRoot.vue"),
        name: "Sources",
        path: "sources",
        meta: { icon: "o_bookmarks" },
        nav: true,
        redirect: "/sources/records",
        children: [
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Archives",
            path: "archives",
            nav: true,
            meta: {
              icon: "o_home_work",
              sourceType: "archives",
              sourceTypeAPI: "archives",
            },
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Archival Files",
            path: "archival-files",
            nav: true,
            meta: {
              icon: "o_inventory_2",
              sourceType: "archivalFiles",
              sourceTypeAPI: "archival_files",
            },
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Records",
            path: "records",
            nav: true,
            meta: {
              icon: "o_text_snippet",
              sourceType: "records",
              sourceTypeAPI: "records",
            },
          },
          {
            component: () => import("pages/source-list/SourceList.vue"),
            name: "Bibliography",
            path: "bibilographies",
            nav: true,
            meta: {
              icon: "o_local_library",
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
        meta: { icon: "o_folder_copy" },
        nav: true,
        redirect: "/sets/datasets",
        children: [
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Corpora",
            path: "corpora",
            nav: true,
            meta: {
              icon: "o_drive_folder_upload",
              setType: "corpora",
              setTypeAPI: "corpora",
            },
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Collections",
            path: "collections",
            nav: true,
            meta: {
              icon: "o_folder_special",
              setType: "collections",
              setTypeAPI: "collections",
            },
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Datasets",
            path: "datasets",
            nav: true,
            meta: {
              icon: "o_topic",
              setType: "datasets",
              setTypeAPI: "datasets",
            },
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Worksets",
            path: "worksets",
            nav: true,
            meta: {
              icon: "o_rule_folder",
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
        meta: { icon: "o_hive" },
        nav: true,
        redirect: "/entities/agents",
        children: [
          {
            component: () => import("pages/agent-list/AgentList.vue"),
            name: "Agents",
            path: "agents",
            meta: { icon: "o_groups" },
            nav: true,
          },
          {
            component: () => import("pages/place-list/PlaceList.vue"),
            name: "Places",
            path: "places",
            meta: { icon: "o_place" },
            nav: true,
          },
        ],
      },

      {
        // Project
        component: () => import("pages/project-root/ProjectRoot.vue"),
        name: "Project",
        path: "project",
        meta: { icon: "o_business_center" },
        nav: true,
        redirect: "/project/tasks",
        children: [
          {
            component: () => import("pages/task-list/TaskList.vue"),
            name: "Tasks",
            path: "tasks",
            meta: { icon: "checklist" },
            nav: true,
          },
          {
            component: () => import("pages/ticket-list/TicketList.vue"),
            name: "Tickets",
            path: "tickets",
            meta: { icon: "o_bug_report" },
            nav: true,
          },
          {
            component: () => import("pages/library-list/LibraryList.vue"),
            name: "Library",
            path: "library",
            meta: { icon: "menu_book" },
            nav: true,
          },
          {
            component: () => import("pages/rights-list/RightsList.vue"),
            name: "Rights Policies",
            path: "rights",
            meta: { icon: "copyright" },
            nav: true,
          },
        ],
      },

      {
        // System
        component: () => import("pages/system-root/SystemRoot.vue"),
        name: "System",
        path: "system",
        meta: { icon: "o_settings_applications" },
        nav: true,
        redirect: "/system/locales",
        children: [
          {
            component: () => import("pages/locale-list/LocaleList.vue"),
            name: "Locales",
            path: "locales",
            meta: { icon: "location_city" },
            nav: true,
          },
          {
            component: () => import("pages/country-list/CountryList.vue"),
            name: "Countries",
            path: "countries",
            meta: { icon: "o_flag" },
            nav: true,
          },
          {
            component: () => import("pages/language-list/LanguageList.vue"),
            name: "Languages",
            path: "languages",
            meta: { icon: "o_g_translate" },
            nav: true,
          },
          {
            component: () => import("pages/user-list/UserList.vue"),
            name: "Users",
            path: "users",
            meta: { icon: "o_supervisor_account" },
            nav: true,
          },
          {
            component: {},
            name: "Admin",
            path: "admin",
            meta: { icon: "o_admin_panel_settings" },
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
          icon: "attribution",
        },
      },
      {
        component: () => import("pages/set/Set.vue"),
        name: "Set",
        path: "sets/:id",
        nav: false,
        meta: {
          navPath: ["Sets"],
          icon: "o_folder",
        },
      },
      {
        component: () => import("pages/source/Source.vue"),
        name: "Source",
        path: "sources/:id",
        nav: false,
        meta: {
          navPath: ["Sources"],
          icon: "bookmark_border",
        },
      },
      {
        component: () => import("pages/task/Task.vue"),
        name: "Task",
        path: "tasks/:id",
        nav: false,
        meta: {
          navPath: ["Project", "Tasks"],
          icon: "add_task",
        },
      },
      {
        component: () => import("pages/ticket/Ticket.vue"),
        name: "Ticket",
        path: "tickets/:id",
        nav: false,
        meta: {
          navPath: ["Project", "Tickets"],
          icon: "o_pest_control",
        },
      },
      {
        component: () => import("pages/user/User.vue"),
        name: "User",
        path: "system/users/:username",
        nav: false,
        meta: {
          navPath: ["System", "Users"],
          icon: "person_outline",
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
