<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-card-section>
        <div class="row">
          <div class="text-h6">Task Lists</div>

          <q-btn
            round
            class="q-ml-auto"
            size="sm"
            :icon="showing ? 'visibility_off' : 'visibility'"
            @click.stop="showing = !showing"
          >
            <q-tooltip class="bg-blue">
              {{ showing ? "Hide task lists" : "Show task lists" }}
            </q-tooltip>
          </q-btn>

          <q-btn
            v-if="isAdmin"
            round
            color="amber"
            text-color="black"
            icon="add"
            size="sm"
            class="q-ml-sm"
            @click.stop="handleCreate"
          >
            <q-tooltip class="bg-blue"> Create Task List </q-tooltip>
          </q-btn>
        </div>
      </q-card-section>

      <q-list
        v-show="showing"
        v-for="(list, group, idx) in taskLists"
        :key="idx"
      >
        <q-separator />

        <q-item-label
          clickable
          header
          class="group"
          style="cursor: pointer"
          v-ripple.center="{ color: 'yellow' }"
          :group="group"
          :class="{ active: activeFilters && activeFilters.has(group) }"
          @click.stop="filter"
        >
          {{ group }}
        </q-item-label>

        <q-separator />

        <q-item
          clickable
          class="list"
          v-ripple:yellow
          v-for="(taskList, idx) in list"
          :key="idx"
          :group="group"
          :list="taskList.name"
          :active="
            activeFilters && activeFilters.has(`${group}_${taskList.name}`)
          "
          active-class="bg-teal-1 text-grey-8"
          @click.stop="filter"
        >
          <q-item-section>{{ taskList.name }}</q-item-section>

          <q-item-section>
            <q-badge
              transparent
              color="primary"
              class="q-ml-auto"
              :label="taskList.taskCount"
            />
          </q-item-section>

          <q-item-section class="col-grow" v-if="isAdmin">
            <div class="row q-ml-sm">
              <q-btn
                round
                color="amber"
                text-color="black"
                icon="edit"
                size="xs"
                class="q-ml-auto q-mr-xs"
                @click.stop="handleEdit(taskList)"
              >
                <q-tooltip
                  class="bg-blue"
                  anchor="center left"
                  self="center right"
                  :offset="[10, 10]"
                >
                  Edit task list
                </q-tooltip>
              </q-btn>

              <q-btn
                round
                text-color="black"
                icon="delete"
                size="xs"
                @click.stop="handleDelete(taskList)"
                :color="taskList.taskCount === 0 ? 'amber' : 'grey'"
                :disabled="taskList.taskCount > 0"
              >
                <q-tooltip
                  v-if="taskList.taskCount === 0"
                  class="bg-blue"
                  transition-show="scale"
                  transition-hide="scale"
                  anchor="center left"
                  self="center right"
                  :offset="[10, 10]"
                >
                  Delete task list
                </q-tooltip>
              </q-btn>
            </div>
          </q-item-section>
        </q-item>
      </q-list>
    </q-card>
  </div>
</template>

<script>
import cuid from "cuid";
import { computed, defineComponent, inject, ref } from "vue";
import { useRouter } from "vue-router";

import { requests } from "@/api";
import { useAPI, useEditing, useNotifier, usePermissions } from "@/use";

export default defineComponent({
  name: "TaskLists",
  emits: ["onReload"],
  setup(_, context) {
    const $notifier = useNotifier();
    const $router = useRouter();
    const {
      machine: { send },
    } = useEditing();
    const {
      permissions: { isAdmin },
    } = usePermissions();

    const title = "Task Lists";
    const activeFilters = ref(new Set());
    const showing = ref(false);
    const taskLists = inject("taskLists");

    const filter = (e) => {
      let group = e.currentTarget.getAttribute("group");
      let list = e.currentTarget.getAttribute("list");

      const { filter } = $router.currentRoute.value.query;
      const prevFilter = filter ? new Set(filter.split(",")) : new Set();
      const clicked = list ? `${group}_${list}` : group;
      prevFilter.has(clicked)
        ? prevFilter.delete(clicked)
        : prevFilter.add(clicked);

      if (list && prevFilter.has(group)) prevFilter.delete(group);
      if (group && !list) {
        for (let item of prevFilter) {
          if (item.startsWith(`${group}_`)) {
            prevFilter.delete(item);
          }
        }
      }

      activeFilters.value = prevFilter;
      const newFilters = Array.from(prevFilter).join(",");

      $router.push({
        query: { ...(newFilters && { filter: newFilters }) },
      });
    };

    const isFiltered = computed(() => $router.currentRoute.value.query.filter);
    if (isFiltered.value) {
      activeFilters.value = new Set(isFiltered.value.split(","));
      showing.value = true;
    }

    // TODO: Need to reload on create.
    const handleCreate = () =>
      send("SPAWN_FORM", {
        cuid: cuid(),
        initialData: {},
        kind: "taskList",
        mode: "create",
      });

    const handleEdit = (taskList) =>
      send("SPAWN_FORM", {
        cuid: cuid(),
        initialData: taskList,
        kind: "taskList",
        mode: "update",
      });

    const handleDelete = (taskList) => {
      const { success, fetchAPI } = useAPI(context);
      const request = requests.tasks.deleteTaskList(taskList.id);
      fetchAPI(request).then(() => {
        if (success.value) {
          $notifier.tasks.taskListDeleted(taskList.name);
          context.emit("onReload");
        }
      });
    };

    return {
      activeFilters,
      filter,
      handleCreate,
      handleEdit,
      handleDelete,
      isAdmin,
      showing,
      taskLists,
      title,
    };
  },
});
</script>

<style lang="scss" scoped>
.group.active {
  background: #e0f2f1 !important;
  color: #616161 !important;
}
.group:hover {
  background-color: rgba(255, 190, 190, 0.1);
  transition: color 0.3s, background-color 0.3s;
}
</style>
