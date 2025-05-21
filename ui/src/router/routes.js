import { Tasks } from "@/models/task";

const routes = [
  {
    name: "Home",
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        component: () => import("pages/Dashboard.vue"),
        name: "Dashboard",
        path: "",
        meta: {
          navPath: ["Dashboard", null],
          icon: "mdi-view-dashboard-outline",
          pageIcon: "mdi-view-dashboard",
        },
        menu: "menu",
      },
      {
        // Records
        component: () => import("pages/Records.vue"),
        path: "records",
        menu: "menu",
        meta: {
          navPath: ["Records", null],
          icon: "mdi-text-box-outline",
          pageIcon: "mdi-text-box",
        },
        children: [
          {
            component: () => import("components/record-list/RecordList.vue"),
            name: "Records",
            path: "",
          },
          {
            component: () => import("components/record-detail/RecordDetail.vue"),
            name: "Record",
            path: ":id",
            meta: {
              viewDefaults: { tab: "info" },
              viewDefaultState: "recordDetail",
            },
          },
        ],
      },
      {
        // Collections
        component: () => import("pages/RecordGroups.vue"),
        path: "record-groups",
        menu: "menu",
        meta: {
          navPath: ["Record Groups", null],
          icon: "mdi-archive-outline",
          pageIcon: "mdi-archive",
        },
        children: [
          {
            component: () => import("components/record-group-list/RecordGroupList.vue"),
            name: "Record Groups",
            path: "",
          },
          {
            component: () => import("components/record-group-detail/RecordGroupDetail.vue"),
            name: "Record Group",
            path: ":id",
            meta: {
              viewDefaults: { tab: "info" },
            },
          },
        ],
      },
      {
        // Images
        component: () => import("pages/Entities.vue"),
        name: "Images",
        path: "images",
        meta: {
          navPath: ["Images", null],
          icon: "mdi-image-multiple-outline",
          pageIcon: "mdi-image-multiple",
        },
        menu: "menu",
      },
      {
        // Entities
        component: () => import("pages/Entities.vue"),
        name: "Entities",
        path: "entities",
        menu: "app",
        children: [
          {
            component: () => import("pages/Agents.vue"),
            name: "Agents",
            path: "agents",
            meta: {
              navPath: ["Entities", "Agents"],
              icon: "mdi-account-child-outline",
              pageIcon: "mdi-account-child",
            },
          },
          {
            component: () => import("pages/Places.vue"),
            name: "Places",
            path: "places",
            meta: {
              navPath: ["Entities", "Places"],
              icon: "mdi-map-marker-multiple-outline",
              pageIcon: "mdi-map-marker-multiple",
            },
          },
          {
            component: () => import("pages/Places.vue"),
            name: "Objects",
            path: "objects",
            meta: {
              navPath: ["Entities", "Objects"],
              icon: "mdi-atom",
            },
          },
        ],
      },
      {
        // Reference
        component: () => import("pages/System.vue"),
        name: "Reference",
        path: "Reference",
        menu: "app",
        children: [
          {
            component: () => import("pages/Countries.vue"),
            name: "Countries",
            path: "countries",
            meta: {
              navPath: ["Reference", "Countries"],
              icon: "mdi-earth",
            },
          },
          {
            component: () => import("pages/Languages.vue"),
            name: "Languages",
            path: "languages",
            meta: {
              navPath: ["Reference", "Languages"],
              icon: "mdi-translate",
            },
          },
          {
            component: () => import("pages/Library.vue"),
            name: "Library",
            path: "library",
            meta: {
              navPath: ["Reference", "Library"],
              icon: "mdi-bookshelf",
            },
          },
          {
            component: () => import("pages/Locales.vue"),
            name: "Locales",
            path: "locales",
            meta: {
              navPath: ["Reference", "Locales"],
              icon: "mdi-office-building-marker-outline",
              pageIcon: "mdi-office-building-marker",
            },
          },
        ],
      },
      {
        // Project
        component: () => import("pages/Project.vue"),
        name: "Project",
        path: "project",
        menu: "app",
        meta: {
          navPath: ["Project", null],
        },
        children: [
          {
            component: () => import("pages/Rights.vue"),
            path: "rights",
            meta: {
              navPath: ["Project", "Rights Policies"],
              icon: "mdi-copyright",
            },
            children: [
              {
                component: () => import("src/components/rights-list/RightsList.vue"),
                name: "Rights Policies",
                path: "",
              },
              {
                component: () => import("src/components/rights-detail/RightsDetail.vue"),
                name: "Rights Policy",
                path: ":id",
                meta: {
                  viewDefaults: { tab: "info" },
                },
              },
            ],
          },
          {
            component: () => import("src/components/rights-list/RightsList.vue"),
            name: "Ontology",
            label: "Edit ontology",
            path: "ontology",
            meta: {
              navPath: ["Project", "Ontology"],
              icon: "mdi-graph-outline",
              pageIcon: "mdi-graph",
            },
          },
        ],
      },
      {
        // Tasks
        component: {},
        name: "Tasks",
        path: "tasks/:id?",
        menu: "top",
        dropdown: false,
        label: "Manage tasks",
        meta: {
          navPath: ["Tasks", null],
          icon: "mdi-format-list-checkbox",
        },
        beforeEnter(to, from) {
          if (from.name == undefined) {
            const state = { showTasks: true };
            if ("id" in to.params) state["taskId"] = to.params.id;
            return { name: "Dashboard", state: state };
          } else {
            if ("id" in to.params) Tasks.setCurrent(to.params.id, true);
            Tasks.showModal();
            return false;
          }
        },
      },
      {
        // Tickets
        component: () => import("pages/Tickets.vue"),
        path: "tickets",
        menu: "top",
        dropdown: false,
        label: "Manage issue tickets",
        meta: {
          navPath: ["Tickets", null],
          icon: "mdi-bug",
        },
        children: [
          {
            component: () => import("src/components/ticket-list/TicketList.vue"),
            name: "Tickets",
            path: "",
          },
          {
            component: () => import("components/ticket-detail/TicketDetail.vue"),
            name: "Ticket",
            path: ":id",
          },
        ],
      },
      {
        component: {},
        name: "DALME Knowledge Base",
        path: "kb",
        menu: "top",
        dropdown: false,
        label: "Open DALME Knowledge Base.",
        meta: {
          navPath: ["System", "KB"],
          icon: "mdi-book-open-page-variant-outline",
        },
        beforeEnter(_) {
          window.location.replace("https://kb.dalme.org/");
        },
      },
      {
        // System
        component: () => import("pages/System.vue"),
        path: "system",
        menu: "top",
        dropdown: true,
        meta: {
          navPath: ["System", null],
          icon: "mdi-cog",
        },
        children: [
          {
            component: () => import("pages/Users.vue"),
            path: "users",
            separator: false,
            meta: {
              navPath: ["System", "Users"],
              icon: "mdi-account-multiple-outline",
              pageIcon: "mdi-account-multiple",
            },
            children: [
              {
                component: () => import("src/components/user-list/UserList.vue"),
                name: "Users",
                label: "Manage users",
                path: "",
              },
              {
                component: () => import("components/user-detail/UserDetail.vue"),
                name: "User",
                path: ":username",
              },
            ],
          },
          {
            component: () => import("src/components/ticket-list/TicketList.vue"),
            name: "Groups",
            label: "Manage groups and teams",
            path: "groups",
            separator: true,
            meta: {
              navPath: ["System", "Groups"],
              icon: "mdi-account-group-outline",
              pageIcon: "mdi-account-group",
            },
          },
          {
            component: () => import("src/components/ticket-list/TicketList.vue"),
            name: "Permissions",
            label: "Manage permissions",
            path: "permissions",
            separator: true,
            meta: {
              navPath: ["System", "Permissions"],
              icon: "mdi-lock-check-outline",
              pageIcon: "mdi-lock-check",
            },
          },
          {
            component: {},
            name: "Admin",
            label: "Open Django Admin",
            path: "admin",
            meta: {
              navPath: ["System", "Admin"],
              icon: "mdi-application-cog-outline",
              pageIcon: "mdi-application-cog",
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
    name: "HTTP 500",
    path: "/500",
    component: () => import("pages/Error500.vue"),
  },
  {
    name: "HTTP 404",
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
