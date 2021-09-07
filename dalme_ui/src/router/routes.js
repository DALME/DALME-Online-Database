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
        // Sets
        component: () => import("pages/set-root/SetRoot.vue"),
        name: "Sets",
        path: "sets",
        props: { icon: "collections_bookmark" },
        nav: true,
        redirect: "/sets/datasets",
        children: [
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Corpora",
            path: "corpora",
            props: { icon: "collections" },
            nav: true,
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Collections",
            path: "collections",
            props: { icon: "collections" },
            nav: true,
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Datasets",
            path: "datasets",
            props: { icon: "collections" },
            nav: true,
          },
          {
            component: () => import("pages/set-list/SetList.vue"),
            name: "Worksets",
            path: "worksets",
            props: { icon: "collections" },
            nav: true,
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
            props: { icon: "recent_actors" },
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
        props: { icon: "settings" },
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
            props: { icon: "groups" },
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
      // TODO: Should be able to scope these to children...
      {
        component: () => import("pages/language/Language.vue"),
        name: "Language",
        path: "languages/:objId",
        nav: false,
      },
      {
        component: () => import("pages/locale/Locale.vue"),
        name: "Locale",
        path: "locales/:objId",
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
        path: "sets/:objId",
        nav: false,
      },
      {
        component: () => import("pages/source/Source.vue"),
        name: "Source",
        path: "sources/:objId",
        nav: false,
      },
      {
        component: () => import("pages/task/Task.vue"),
        name: "Task",
        path: "tasks/:objId",
        nav: false,
      },
      {
        component: () => import("pages/ticket/Ticket.vue"),
        name: "Ticket",
        path: "tickets/:objId",
        nav: false,
      },
      {
        component: () => import("pages/user/User.vue"),
        name: "User",
        path: "users/:username",
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
