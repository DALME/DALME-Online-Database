<template>
  <q-btn-dropdown
    label="Lists"
    size="12px"
    menu-anchor="bottom left"
    menu-self="top left"
    content-class="popup-menu filtered dark info-list"
  >
    <q-list separator>
      <q-item dense class="header">
        <q-item-section>Task lists</q-item-section>
        <q-item-section side>
          <q-btn flat dense size="xs" icon="close" @click.stop="tm.clearListFilters" />
        </q-item-section>
      </q-item>

      <template v-for="(list, group, idx) in lists" :key="idx">
        <q-item
          dense
          clickable
          :group="group"
          :active="tm.activeGroups.has(group)"
          @click.stop="tm.setFilterList(group, true)"
        >
          <q-item-section avatar>
            <q-icon name="mdi-account-group-outline" size="xs" />
          </q-item-section>
          <q-item-section>
            {{ `${group} group` }}
          </q-item-section>
        </q-item>

        <q-item
          v-for="(taskList, idx) in list"
          :key="idx"
          dense
          clickable
          class="inset-item"
          :group="group"
          :list="taskList.name"
          :active="tm.activeGroups.has(group) || tm.activeLists.has(`${group}-${taskList.name}`)"
          @click.stop="tm.setFilterList(`${group}-${taskList.name}`)"
        >
          <q-item-section>
            {{ taskList.name }}
          </q-item-section>
          <q-item-section class="badges">
            <q-badge
              rounded
              outline
              :label="taskList.taskCount"
              :color="taskList.taskCount > 0 ? 'light-green-8' : 'blue-grey-8'"
            />
          </q-item-section>
          <q-item-section side class="actions">
            <q-btn v-if="isAdmin" flat dense size="sm" icon="mdi-pencil-outline">
              <TooltipWidget anchor="center left" self="center right" :offset="[10, 10]">
                Edit task list
              </TooltipWidget>
            </q-btn>

            <q-btn
              v-if="isAdmin"
              flat
              dense
              size="sm"
              icon="mdi-delete-forever-outline"
              :disable="taskList.taskCount > 0"
            >
              <TooltipWidget
                v-if="taskList.taskCount === 0"
                anchor="center left"
                self="center right"
                :offset="[10, 10]"
              >
                Delete task list
              </TooltipWidget>
            </q-btn>
          </q-item-section>
        </q-item>
      </template>

      <q-item v-if="isAdmin" clickable v-close-popup dense>
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
import { TooltipWidget } from "@/components";
import { useAuthStore } from "@/stores/auth";
import { useTasks } from "@/stores/tasks";

export default defineComponent({
  name: "TasklistList",
  props: {
    lists: {
      type: Object,
      required: true,
    },
  },
  components: {
    TooltipWidget,
  },
  emits: ["onReload"],
  setup() {
    const auth = useAuthStore();
    const title = "Task Lists";
    const tm = useTasks();

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
      tm,
    };
  },
});
</script>
