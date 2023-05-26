const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        component: () => import("pages/Dashboard.vue"),
        name: "Dashboard",
        path: "",
        meta: {
          navPath: ["Dashboard", null],
          icon: "o_space_dashboard",
        },
        nav: true,
      },

      /* Sections */
      {
        // Sources
        component: () => import("pages/Sources.vue"),
        name: "Sources",
        path: "sources",
        meta: {
          navPath: ["Sources", null],
          icon: "o_bookmarks",
        },
        nav: true,
        children: [
          {
            component: () =>
              import("src/components/source-list/SourceList.vue"),
            name: "Archives",
            path: "archives",
            nav: true,
            meta: {
              navPath: ["Sources", "Archives"],
              icon: "o_home_work",
              sourceType: "archives",
              sourceTypeAPI: "archives",
            },
          },
          {
            component: () =>
              import("src/components/source-list/SourceList.vue"),
            name: "Archival Files",
            path: "archival-files",
            nav: true,
            meta: {
              navPath: ["Sources", "Archival Files"],
              icon: "o_inventory_2",
              sourceType: "archivalFiles",
              sourceTypeAPI: "archival_files",
            },
          },
          {
            component: () =>
              import("src/components/source-list/SourceList.vue"),
            name: "Records",
            path: "records",
            nav: true,
            meta: {
              navPath: ["Sources", "Records"],
              icon: "o_text_snippet",
              sourceType: "records",
              sourceTypeAPI: "records",
            },
          },
          {
            component: () =>
              import("src/components/source-list/SourceList.vue"),
            name: "Bibliography",
            path: "bibilographies",
            nav: true,
            meta: {
              navPath: ["Sources", "Bibliography"],
              icon: "o_local_library",
              sourceType: "bibliography",
              sourceTypeAPI: "bibliography",
            },
          },
          {
            component: () =>
              import("components/source-detail/SourceDetail.vue"),
            name: "Source",
            path: ":id",
            nav: false,
            meta: {
              navPath: ["Sources", null],
              icon: "bookmark_border",
              allowCompactMode: true,
              viewDefaults: { tab: "info" },
            },
          },
        ],
      },

      {
        // Sets
        component: () => import("pages/Sets.vue"),
        name: "Sets",
        path: "sets",
        meta: {
          navPath: ["Sets", null],
          icon: "o_folder_copy",
        },
        nav: true,
        children: [
          {
            component: () => import("src/components/set-list/SetList.vue"),
            name: "Corpora",
            path: "corpora",
            nav: true,
            meta: {
              navPath: ["Sets", "Corpora"],
              icon: "o_drive_folder_upload",
              setType: "corpora",
              setTypeAPI: "corpora",
            },
          },
          {
            component: () => import("src/components/set-list/SetList.vue"),
            name: "Collections",
            path: "collections",
            nav: true,
            meta: {
              navPath: ["Sets", "Collections"],
              icon: "o_folder_special",
              setType: "collections",
              setTypeAPI: "collections",
            },
          },
          {
            component: () => import("src/components/set-list/SetList.vue"),
            name: "Datasets",
            path: "datasets",
            nav: true,
            meta: {
              navPath: ["Sets", "Datasets"],
              icon: "o_topic",
              setType: "datasets",
              setTypeAPI: "datasets",
            },
          },
          {
            component: () => import("src/components/set-list/SetList.vue"),
            name: "Worksets",
            path: "worksets",
            nav: true,
            meta: {
              navPath: ["Sets", "Worksets"],
              icon: "o_rule_folder",
              setType: "worksets",
              setTypeAPI: "worksets",
            },
          },
          {
            component: () => import("components/set-detail/SetDetail.vue"),
            name: "Set",
            path: ":id",
            nav: false,
            meta: {
              navPath: ["Sets", null],
              icon: "o_folder",
              allowCompactMode: true,
              preserveCompactMode: true,
            },
          },
        ],
      },

      {
        // Entities
        component: () => import("pages/Entities.vue"),
        name: "Entities",
        path: "entities",
        meta: {
          navPath: ["Entities", null],
          icon: "o_hive",
        },
        nav: true,
        children: [
          {
            component: () => import("pages/Agents.vue"),
            name: "Agents",
            path: "agents",
            nav: true,
            meta: {
              navPath: ["Entities", "Agents"],
              icon: "o_groups",
            },
          },
          {
            component: () => import("pages/Places.vue"),
            name: "Places",
            path: "places",
            nav: true,
            meta: {
              navPath: ["Entities", "Places"],
              icon: "o_place",
            },
          },
        ],
      },

      {
        // Project
        component: () => import("pages/Project.vue"),
        name: "Project",
        path: "project",
        meta: {
          navPath: ["Project", null],
          icon: "o_business_center",
        },
        nav: true,
        children: [
          {
            component: () => import("pages/Tasks.vue"),
            path: "tasks",
            nav: true,
            children: [
              {
                component: () =>
                  import("src/components/task-list/TaskList.vue"),
                name: "Tasks",
                path: "",
                nav: true,
                meta: {
                  navPath: ["Project", "Tasks"],
                  icon: "checklist",
                },
              },
              {
                component: () =>
                  import("components/task-detail/TaskDetail.vue"),
                name: "Task",
                path: ":id",
                nav: false,
                meta: {
                  navPath: ["Project", "Tasks"],
                  icon: "add_task",
                  allowCompactMode: false,
                  preserveCompactMode: false,
                },
              },
            ],
          },
          {
            component: () => import("pages/Tickets.vue"),
            path: "tickets",
            nav: true,
            children: [
              {
                component: () =>
                  import("src/components/ticket-list/TicketList.vue"),
                name: "Tickets",
                path: "",
                nav: true,
                meta: {
                  navPath: ["Project", "Tickets"],
                  icon: "o_bug_report",
                },
              },
              {
                component: () =>
                  import("components/ticket-detail/TicketDetail.vue"),
                name: "Ticket",
                path: ":id",
                nav: false,
                meta: {
                  navPath: ["Project", "Tickets"],
                  icon: "o_pest_control",
                  allowCompactMode: false,
                  preserveCompactMode: false,
                },
              },
            ],
          },
          {
            component: () => import("pages/Library.vue"),
            name: "Library",
            path: "library",
            nav: true,
            meta: {
              navPath: ["Project", "Library"],
              icon: "menu_book",
            },
          },
          {
            component: () => import("pages/Rights.vue"),
            path: "rights",
            nav: true,
            children: [
              {
                component: () =>
                  import("src/components/rights-list/RightsList.vue"),
                name: "Rights Policies",
                path: "",
                nav: true,
                meta: {
                  navPath: ["Project", "Rights Policies"],
                  icon: "copyright",
                },
              },
              {
                component: () =>
                  import("components/rights-detail/RightsDetail.vue"),
                name: "Rights",
                path: ":id",
                props: true,
                nav: false,
                meta: {
                  navPath: ["Project", "Rights Policies"],
                  icon: "attribution",
                  allowCompactMode: false,
                  preserveCompactMode: false,
                },
              },
            ],
          },
        ],
      },

      {
        // System
        component: () => import("pages/System.vue"),
        name: "System",
        path: "system",
        meta: {
          navPath: ["System", null],
          icon: "o_settings_applications",
        },
        nav: true,
        children: [
          {
            component: () => import("pages/Locales.vue"),
            name: "Locales",
            path: "locales",
            nav: true,
            meta: {
              navPath: ["System", "Locales"],
              icon: "location_city",
            },
          },
          {
            component: () => import("pages/Countries.vue"),
            name: "Countries",
            path: "countries",
            nav: true,
            meta: {
              navPath: ["System", "Countries"],
              icon: "o_flag",
            },
          },
          {
            component: () => import("pages/Languages.vue"),
            name: "Languages",
            path: "languages",
            nav: true,
            meta: {
              navPath: ["System", "Languages"],
              icon: "o_g_translate",
            },
          },
          {
            component: () => import("pages/Users.vue"),
            path: "users",
            nav: true,
            children: [
              {
                component: () =>
                  import("src/components/user-list/UserList.vue"),
                name: "Users",
                path: "",
                nav: true,
                meta: {
                  navPath: ["System", "Users"],
                  icon: "o_supervisor_account",
                },
              },
              {
                component: () =>
                  import("components/user-detail/UserDetail.vue"),
                name: "User",
                path: ":username",
                nav: false,
                meta: {
                  navPath: ["System", "Users"],
                  icon: "person_outline",
                  allowCompactMode: false,
                  preserveCompactMode: false,
                },
              },
            ],
          },
          {
            component: {},
            name: "Admin",
            path: "admin",
            nav: true,
            meta: {
              navPath: ["System", "Admin"],
              icon: "o_admin_panel_settings",
            },
            beforeEnter(_) {
              window.location.replace("/admin");
            },
          },
        ],
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
