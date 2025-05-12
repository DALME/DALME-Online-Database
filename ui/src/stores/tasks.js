import { defineStore } from "pinia";
import { Dialog } from "quasar";
import { computed, defineAsyncComponent, ref } from "vue";
import { useRouter } from "vue-router";

import { API as apiInterface, requests } from "@/api";
import { TaskLists, Tasks } from "@/models";
import { taskListsSchema, tasksSchema } from "@/schemas";
import { useAuthStore } from "@/stores/auth";

export const useTaskStore = defineStore(
  "tasks",
  () => {
    // stores and repositories
    const auth = useAuthStore();
    const $router = useRouter();

    // state
    const ready = ref(false);
    const timestamp = ref(null);
    const loading = ref(false);
    const onViewer = ref(null);
    const activeFilters = ref(new Set());
    const activeGroups = ref(new Set());
    const activeLists = ref(new Set());
    const activeSort = ref("");
    const meta = ref({ all: 0, user: 0, created: 0, assigned: 0, completed: 0 });
    const showCount = ref({ all: 5, created: 5, assigned: 5, completed: 5 });

    const request = {
      list: {
        user: requests.taskLists.getByUser,
        null: requests.taskLists.list,
      },
      task: {
        user: requests.tasks.getByUser,
        null: requests.tasks.list,
        assigned: requests.tasks.getAssigned,
        completed: requests.tasks.getCompleted,
        created: requests.tasks.getCreated,
      },
    };

    const schemas = {
      list: taskListsSchema,
      task: tasksSchema,
    };

    // getters
    const isStale = computed(() => Date.now() - timestamp.value > 86400000);
    const moreTasks = computed(() => showCount.value.all < meta.value.all);
    const moreAssigned = computed(() => showCount.value.assigned < meta.value.assigned);
    const moreCompleted = computed(() => showCount.value.completed < meta.value.completed);
    const moreCreated = computed(() => showCount.value.created < meta.value.created);

    const assigned = computed(() =>
      Tasks.withAllRecursive().where("isAssignee", true).limit(showCount.value.assigned).get(),
    );
    const completed = computed(() =>
      Tasks.withAllRecursive().where("completed", true).limit(showCount.value.completed).get(),
    );
    const created = computed(() =>
      Tasks.withAllRecursive()
        .where((q) => q.isAuthor === true && q.isAssignee === false && q.completed === false)
        .limit(showCount.value.created)
        .get(),
    );

    const listGroups = computed(() => Tasks.withAllRecursive().groupBy("teamLink.name").get());

    const loaded = computed(() => {
      return {
        all: Tasks.all().length,
        assigned: assigned.value.length,
        completed: completed.value.length,
        created: created.value.length,
      };
    });

    // actions
    const initialize = () => {
      // temp testing
      Tasks.remoteListByUser(auth.user.id);
      // end temp
      $reset();
      loading.value = true;
      return new Promise((resolve) => {
        fetchData(TaskLists, "list", "user", null, 50).then(() => {
          fetchData(Tasks, "task", "user", null, 15).then((data) => {
            const state = $router.options.history.state;
            timestamp.value = Date.now();
            meta.value.all = data.totalTasks;
            meta.value.user = data.count;
            meta.value.created = data.totalCreated;
            meta.value.assigned = data.totalAssigned;
            meta.value.completed = data.totalCompleted;
            if ("taskId" in state) setViewer(state.taskId);
            if ("showTasks" in state) showTaskModal();
            ready.value = true;
            loading.value = false;
            return resolve(true);
          });
        });
      });
    };

    const $reset = () => {
      ready.value = false;
      timestamp.value = null;
      loading.value = false;
      meta.value = {
        all: 0,
        user: 0,
        created: 0,
        assigned: 0,
        completed: 0,
      };
    };

    const getRequest = (resource, type, query, limit = 0, offset = 0) => {
      const target = query ? query : auth.user.id;
      return request[resource][type](target, limit, offset);
    };

    const fetchData = (repository, resource, type = null, query = null, limit = 0, offset = 0) => {
      return new Promise((resolve) => {
        const { success, data, fetchAPI } = apiInterface();
        loading.value = true;
        const request = getRequest(resource, type, query, limit, offset);
        const schema = schemas[resource];
        fetchAPI(request).then(() => {
          if (success.value) {
            schema.validate(data.value.data, { stripUnknown: true }).then((response) => {
              repository.save(response).then((ret) => {
                console.log("SAVED", resource, ret);
                resolve(data.value);
              });
            });
          }
        });
      });
    };

    const tasks = (query = null) => {
      if (!query) {
        return Tasks.with("creationUser")
          .with("modificationUser")
          .with("completedBy")
          .with("assignees")
          .orderBy("creationTimestamp")
          .get();
      } else {
        if (typeof query === "string") {
          return Tasks.with("creationUser")
            .with("modificationUser")
            .with("completedBy")
            .with("assignees")
            .where(
              (q) =>
                q.title.toLowerCase().includes(query.toLowerCase()) ||
                q.description.toLowerCase().includes(query.toLowerCase()),
            )
            .get();
        } else if (typeof query === "number") {
          return Tasks.with("creationUser")
            .with("modificationUser")
            .with("completedBy")
            .with("assignees")
            .find(query);
        }
      }
    };

    const lists = (query = null) => {
      if (!query) {
        return TaskLists.with("creationUser").with("modificationUser").with("owner").all();
      } else {
        if (typeof query === "string") {
          return TaskLists.with("creationUser")
            .with("modificationUser")
            .with("owner")
            .where(
              (q) =>
                q.name.toLowerCase().includes(query.toLowerCase()) ||
                q.description.toLowerCase().includes(query.toLowerCase()),
            )
            .get();
        } else if (typeof query === "number") {
          return TaskLists.with("creationUser").with("modificationUser").with("owner").find(query);
        }
      }
    };

    const setViewer = (task) => {
      const target = typeof task === "number" ? tasks(task) : task;
      onViewer.value = target;
    };

    const showTaskModal = () => {
      Dialog.create({
        component: defineAsyncComponent(() => import("components/task-manager/TaskViewer.vue")),
      });
    };

    const onShowMore = (type) => {
      let target =
        showCount.value[type] + 1 >= meta.value[type]
          ? meta.value[type]
          : (showCount.value[type] += 1);

      if (target > loaded.value[type] && loaded.value[type] < meta.value[type] && !loading.value) {
        fetchData(Tasks, "task", type, 1, loaded.value[type]).then(() => {
          showCount.value[type] = target;
          loading.value = false;
        });
      }
    };

    const clearFilters = () => {
      activeFilters.value.clear();
    };

    const clearListFilters = () => {
      activeGroups.value.clear();
      activeLists.value.clear();
    };

    const setFilterList = (value, isGroup = false) => {
      if (isGroup) {
        if (activeGroups.value.has(value)) {
          activeGroups.value.delete(value);
          lists.index[value].forEach((x) => activeLists.value.delete(`${value}-${x}`));
        } else {
          activeGroups.value.add(value);
          lists.index[value].forEach((x) => activeLists.value.add(`${value}-${x}`));
        }
      } else {
        if (activeLists.value.has(value)) {
          activeLists.value.delete(value);
        } else {
          activeLists.value.add(value);
        }
      }
    };

    return {
      initialize,
      isStale,
      ready,
      loading,
      tasks,
      lists,
      moreTasks,
      moreAssigned,
      moreCompleted,
      moreCreated,
      setViewer,
      showTaskModal,
      meta,
      onShowMore,
      assigned,
      completed,
      created,
      onViewer,
      listGroups,
      activeFilters,
      activeGroups,
      activeLists,
      activeSort,
      setFilterList,
      clearFilters,
      clearListFilters,
      timestamp,
    };
  },
  {
    persist: true,
  },
);
