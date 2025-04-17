import { defineStore } from "pinia";
import { computed, defineAsyncComponent, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRepo } from "pinia-orm";
import { Task, TaskList } from "@/models";
import { API as apiInterface, requests } from "@/api";
import { tasksSchema, taskListsSchema } from "@/schemas";
import { Dialog } from "quasar";
import { useRouter } from "vue-router";

export const useTaskStore = defineStore("tasks", () => {
  // stores and repositories
  const auth = useAuthStore();
  const taskRepo = useRepo(Task);
  const taskListRepo = useRepo(TaskList);
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
      user: requests.tasks.getUserTaskLists,
      null: requests.tasks.getTaskLists,
    },
    task: {
      user: requests.tasks.getUserTasks,
      null: requests.tasks.getTasks,
      assigned: requests.tasks.getAssignedTasks,
      completed: requests.tasks.getCompletedTasks,
      created: requests.tasks.getCreatedTasks,
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
    taskRepo.where("isAssignee", true).limit(showCount.value.assigned).get(),
  );
  const completed = computed(() =>
    taskRepo.where("completed", true).limit(showCount.value.assigned).get(),
  );
  const created = computed(() =>
    taskRepo
      .where((q) => q.isAuthor === true && q.isAssignee === false && q.completed === false)
      .limit(showCount.value.assigned)
      .get(),
  );
  const listGroups = computed(() => taskListRepo.groupBy("teamLink.name").get());

  const loaded = computed(() => {
    return {
      all: taskRepo.all().length,
      assigned: assigned.value.length,
      completed: completed.value.length,
      created: created.value.length,
    };
  });

  // actions
  const initialize = () => {
    return new Promise((resolve) => {
      $reset();
      fetchData(taskListRepo, "list", "user", null, 50).then(() => {
        fetchData(taskRepo, "task", "user", null, 15).then((data) => {
          const state = $router.options.history.state;
          timestamp.value = Date.now();
          meta.value.all = data.totalTasks;
          meta.value.user = data.count;
          meta.value.created = data.totalCreated;
          meta.value.assigned = data.totalAssigned;
          meta.value.completed = data.totalCompleted;
          ready.value = true;
          loading.value = false;
          if ("taskId" in state) setViewer(state.taskId);
          if ("showTasks" in state) showTaskModal();
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
    const target = query ? query : auth.user.userId;
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
            repository.save(response);
            return resolve(data.value);
          });
        }
      });
    });
  };

  const tasks = (query = null) => {
    if (!query) {
      return taskRepo.orderBy("creationTimestamp").get();
    } else {
      if (typeof query === "string") {
        return taskRepo
          .where(
            (q) =>
              q.title.toLowerCase().includes(query.toLowerCase()) ||
              q.description.toLowerCase().includes(query.toLowerCase()),
          )
          .get();
      } else if (typeof query === "number") {
        return taskRepo.find(query);
      }
    }
  };

  const lists = (query = null) => {
    if (!query) {
      return taskListRepo.all();
    } else {
      if (typeof query === "string") {
        return taskListRepo
          .where(
            (q) =>
              q.name.toLowerCase().includes(query.toLowerCase()) ||
              q.description.toLowerCase().includes(query.toLowerCase()),
          )
          .get();
      } else if (typeof query === "number") {
        return taskListRepo.find(query);
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
      fetchData(taskRepo, "task", type, 1, loaded.value[type]).then(() => {
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
  };
});
