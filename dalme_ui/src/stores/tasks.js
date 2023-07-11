import { defineStore } from "pinia";
import { computed, defineAsyncComponent, ref } from "vue";
import { Dialog } from "quasar";
import { useRouter } from "vue-router";
import { useTasklistStore } from "@/stores/tasklist-store";
import { useTaskStore } from "@/stores/task-store";
import { filter as rFilter, groupBy, sortBy, prop, descend } from "ramda";

export const useTasks = defineStore("tasks", () => {
  // stores
  const _tasks = useTaskStore();
  const _lists = useTasklistStore();
  const $router = useRouter();

  // state
  const viewing = ref(null);
  const loadAssigned = ref(5);
  const loadCompleted = ref(5);
  const loadCreated = ref(5);
  const activeFilters = ref(new Set());
  const activeGroups = ref(new Set());
  const activeLists = ref(new Set());
  const activeSort = ref("");
  const show = ref({
    all: 5,
    created: 5,
    assigned: 5,
    completed: 5,
  });
  const presets = ref({
    assigned: [{ prop: "isAssignee", value: true }],
    completed: [{ prop: "completed", value: true }],
    created: [
      { prop: "isAuthor", value: true },
      { prop: "isAssignee", value: false },
      { prop: "completed", value: false },
    ],
  });

  // getters
  const tasksReady = computed(() => _tasks.isLoaded && !_tasks.loading);
  const listsReady = computed(() => _lists.isLoaded && !_lists.loading);
  const tasks = computed(() => _sortByCreationDate(filter().slice(0, show.value.all)));
  const assigned = computed(() => filter(presets.value.assigned).slice(0, show.value.assigned));
  const completed = computed(() => filter(presets.value.completed).slice(0, show.value.completed));
  const created = computed(() => filter(presets.value.created).slice(0, show.value.created));
  const moreTasks = computed(() => show.value.all < _tasks.meta.all);
  const moreAssigned = computed(() => show.value.assigned < _tasks.meta.assigned);
  const moreCompleted = computed(() => show.value.completed < _tasks.meta.completed);
  const moreCreated = computed(() => show.value.created < _tasks.meta.created);
  const listGroups = computed(() => groupBy((x) => x.teamLink.name, _lists.lists));
  const loads = computed(() => {
    return {
      all: tasks.value.length,
      assigned: assigned.value.length,
      completed: completed.value.length,
      created: created.value.length,
    };
  });

  // actions
  const $reset = () => {
    _tasks.$reset();
    _lists.$reset();
  };

  const init = (target = null) => {
    const state = $router.options.history.state;
    if (target == "lists") {
      _lists.init();
    } else {
      _tasks.init().then(() => {
        if (target == null) _lists.init();
        if ("taskId" in state) setViewing(state.taskId, true);
        if ("showTasks" in state) showTaskModal();
      });
    }
  };

  const filter = (passedFilters = null) => {
    if (passedFilters || activeFilters.value.size > 0 || activeLists.value.size > 0) {
      const pred = (x) => {
        if (passedFilters) {
          for (const f of passedFilters) {
            if (prop(f.prop, x) != f.value) return false;
          }
        } else {
          if (activeLists.value.size > 0 && !activeLists.value.has(x.listSlug)) return false;
          if (activeFilters.value.size > 0) {
            for (const f of activeFilters.value) {
              if (prop(f.prop, x) != f.value) return false;
            }
          }
        }
        return true;
      };
      return rFilter(pred, _tasks.tasks);
    } else {
      return _tasks.tasks;
    }
  };

  const setFilterList = (value, isGroup = false) => {
    if (isGroup) {
      if (activeGroups.value.has(value)) {
        activeGroups.value.delete(value);
        _lists.index[value].forEach((x) => activeLists.value.delete(`${value}-${x}`));
      } else {
        activeGroups.value.add(value);
        _lists.index[value].forEach((x) => activeLists.value.add(`${value}-${x}`));
      }
    } else {
      if (activeLists.value.has(value)) {
        activeLists.value.delete(value);
      } else {
        activeLists.value.add(value);
      }
    }
  };

  // const setFilter = () => {

  // };

  const clearFilters = () => {
    activeFilters.value.clear();
  };

  const clearListFilters = () => {
    activeGroups.value.clear();
    activeLists.value.clear();
  };

  const setViewing = (task, byId = false) => {
    const target = byId ? _tasks.getTaskbyId(task) : task;
    viewing.value = target;
  };

  const showTaskModal = () => {
    Dialog.create({
      component: defineAsyncComponent(() => import("components/task-manager/TaskViewer.vue")),
    });
  };

  const onShowMore = (list) => {
    let target =
      show.value[list] + 1 >= _tasks.meta[list] ? _tasks.meta[list] : (show.value[list] += 1);

    if (target > loads.value[list] && loads.value[list] < _tasks.meta[list] && !_tasks.loading) {
      _tasks.fetchData(list, 1, loads.value[list]).then(() => {
        show.value[list] = target;
      });
    }
  };

  const _sortByCreationDate = sortBy(descend(prop("creationTimestamp")));
  const _sortByCompletedDate = sortBy(descend(prop("completedDate")));

  return {
    tasks,
    $reset,
    init,
    assigned,
    completed,
    created,
    loadAssigned,
    loadCompleted,
    loadCreated,
    moreTasks,
    moreAssigned,
    moreCompleted,
    moreCreated,
    onShowMore,
    tasksReady,
    listsReady,
    listGroups,
    viewing,
    setViewing,
    activeGroups,
    activeLists,
    clearFilters,
    clearListFilters,
    setFilterList,
    activeSort,
    showTaskModal,
    tasksMeta: _tasks.meta,
  };
});
