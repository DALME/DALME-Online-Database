<template>
  <q-btn-dropdown
    content-class="popup-menu filtered dark info-list"
    label="Lists"
    menu-anchor="bottom left"
    menu-self="top left"
    size="12px"
  >
    <q-list separator>
      <q-item class="header" dense>
        <q-item-section>Task lists</q-item-section>
        <q-item-section side>
          <q-btn @click.stop="taskStore.clearListFilters" icon="close" size="xs" dense flat />
        </q-item-section>
      </q-item>

      <template v-for="(list, group, idx) in lists" :key="idx">
        <q-item
          @click.stop="taskStore.setFilterList(group, true)"
          :active="taskStore.activeGroups.has(group)"
          :group="group"
          clickable
          dense
        >
          <q-item-section avatar>
            <q-icon name="mdi-account-group-outline" size="xs" />
          </q-item-section>
          <q-item-section>
            {{ `${group} group` }}
          </q-item-section>
        </q-item>

        <q-item
          v-for="(taskList, idx2) in list"
          :key="idx2"
          @click.stop="taskStore.setFilterList(`${group}-${taskList.name}`)"
          :active="
            taskStore.activeGroups.has(group) ||
            taskStore.activeLists.has(`${group}-${taskList.name}`)
          "
          :group="group"
          :list="taskList.name"
          class="inset-item"
          clickable
          dense
        >
          <q-item-section>
            {{ taskList.name }}
          </q-item-section>
          <q-item-section class="badges">
            <q-badge
              :color="taskList.taskCount > 0 ? 'light-green-8' : 'blue-grey-8'"
              :label="taskList.taskCount"
              outline
              rounded
            />
          </q-item-section>
          <q-item-section class="actions" side>
            <q-btn v-if="isAdmin" icon="mdi-pencil-outline" size="sm" dense flat>
              <ToolTip :offset="[10, 10]" anchor="center left" self="center right">
                Edit task list
              </ToolTip>
            </q-btn>

            <q-btn
              v-if="isAdmin"
              :disable="taskList.taskCount > 0"
              icon="mdi-delete-forever-outline"
              size="sm"
              dense
              flat
            >
              <ToolTip
                v-if="taskList.taskCount === 0"
                :offset="[10, 10]"
                anchor="center left"
                self="center right"
              >
                Delete task list
              </ToolTip>
            </q-btn>
          </q-item-section>
        </q-item>
      </template>

      <q-item v-if="isAdmin" v-close-popup clickable dense>
        <q-item-section avatar>
          <q-icon name="mdi-playlist-plus" size="xs" />
        </q-item-section>
        <q-item-section>New Task List</q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
import { defineComponent } from "vue";

import { ToolTip } from "@/components";
import { useAuthStore } from "@/stores/auth";
import { useTaskStore } from "@/stores/tasks";

export default defineComponent({
  name: "TasklistList",
  components: {
    ToolTip,
  },
  props: {
    lists: {
      type: Object,
      required: true,
    },
  },
  emits: ["onReload"],
  setup() {
    const auth = useAuthStore();
    const taskStore = useTaskStore();
    const title = "Task Lists";

    // const filter = (e) => {
    //   let group = e.currentTarget.getAttribute("group");
    //   let list = e.currentTarget.getAttribute("list");

    //   const prevFilter = filter ? new Set(filter.split(",")) : new Set();
    //   const clicked = list ? `${group}_${list}` : group;
    //   prevFilter.has(clicked) ? prevFilter.delete(clicked) : prevFilter.add(clicked);

    //   if (list && prevFilter.has(group)) prevFilter.delete(group);
    //   if (group && !list) {
    //     for (let item of prevFilter) {
    //       if (item.startsWith(`${group}_`)) {
    //         prevFilter.delete(item);
    //       }
    //     }
    //   }

    //   tasks.filters = prevFilter;
    //   const newFilters = Array.from(prevFilter).join(",");
    // };

    // const clearActiveFilters = () => {
    //   filters.value = new Set();
    //   // const { filter } = $router.currentRoute.value.query;
    //   const newFilters = Array.from(filters.value).join(",");
    // };

    return {
      isAdmin: auth.user.isAdmin,
      title,
      taskStore,
    };
  },
});
</script>
