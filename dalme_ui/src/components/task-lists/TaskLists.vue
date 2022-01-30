<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-card-section>
        <div class="row">
          <div class="text-h6">Task Lists</div>
          <q-btn
            v-if="isAdmin"
            round
            color="amber"
            text-color="black"
            icon="add"
            size="sm"
            class="q-ml-auto"
            @click="handleClick"
          >
            <q-tooltip
              class="bg-blue"
              transition-show="scale"
              transition-hide="scale"
              anchor="center left"
              self="center right"
              :offset="[10, 10]"
            >
              Create Task List
            </q-tooltip>
          </q-btn>
        </div>
      </q-card-section>

      <q-list v-for="(list, group, idx) in taskLists" :key="idx">
        <q-separator />

        <q-item-label
          clickable
          header
          class="group"
          style="cursor: pointer"
          v-ripple.center="{ color: 'yellow' }"
          :group="group"
          :class="{ active: activeFilters && activeFilters.has(group) }"
          @click="filter"
        >
          {{ group }}
        </q-item-label>

        <q-separator />

        <q-item
          clickable
          class="list"
          v-ripple:yellow
          v-for="(item, idx) in list"
          :key="idx"
          :group="group"
          :list="item.name"
          :active="activeFilters && activeFilters.has(`${group}_${item.name}`)"
          active-class="bg-teal-1 text-grey-8"
          @click="filter"
        >
          <q-item-section>{{ item.name }}</q-item-section>
          <q-item-section>
            <q-badge
              transparent
              color="primary"
              class="q-ml-auto"
              :label="item.taskCount"
            />
          </q-item-section>
        </q-item>
      </q-list>
    </q-card>
  </div>
</template>

<script>
import cuid from "cuid";
import { defineComponent, inject, ref } from "vue";
import { useRouter } from "vue-router";

import { useEditing, usePermissions } from "@/use";

export default defineComponent({
  name: "TaskLists",
  setup() {
    const $router = useRouter();
    const {
      machine: { send },
    } = useEditing();
    const {
      permissions: { isAdmin },
    } = usePermissions();

    const title = "Task Lists";
    const activeFilters = ref(new Set());
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

    const onLoadFilter = $router.currentRoute.value.query.filter;
    if (onLoadFilter) activeFilters.value = new Set(onLoadFilter.split(","));

    const handleClick = () =>
      send("SPAWN_FORM", {
        cuid: cuid(),
        initialData: {},
        kind: "taskList",
        mode: "create",
      });

    const handleDelete = (id) =>
      console.log(`Deleting TaskList with id: ${id}`);

    return {
      activeFilters,
      filter,
      handleClick,
      handleDelete,
      isAdmin,
      taskLists,
      title,
    };
  },
});
</script>

<style lang="scss">
.group.active {
  background: #e0f2f1 !important;
  color: #616161 !important;
}
.group:hover {
  background-color: rgba(255, 190, 190, 0.1);
  transition: color 0.3s, background-color 0.3s;
}
</style>
