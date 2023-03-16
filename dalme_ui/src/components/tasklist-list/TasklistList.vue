<template>
  <q-btn-dropdown
    unelevated
    no-caps
    label="Task Lists"
    size="12px"
    menu-anchor="bottom left"
    menu-self="top left"
    class="bg-indigo-1 text-indigo-9 table-toolbar-button"
    content-class="menu-shadow"
  >
    <q-list bordered separator class="text-grey-9 task-list-menu">
      <q-item dense class="q-pr-sm">
        <q-item-section class="text-weight-bold">Task lists</q-item-section>
        <q-item-section avatar>
          <q-btn flat dense size="xs" color="grey-6" icon="close" @click="clearActiveFilters" />
        </q-item-section>
      </q-item>

      <template v-for="(list, group, idx) in taskLists" :key="idx">
        <q-item
          dense
          clickable
          :group="group"
          :class="
            activeFilters && activeFilters.has(group)
              ? 'text-weight-bold bg-indigo-1 text-indigo-5'
              : 'text-weight-600 text-grey-7'
          "
          @click.stop="filter"
        >
          <q-item-section side class="q-pr-xs">
            <q-icon name="o_group" size="xs" />
          </q-item-section>
          <q-item-section class="text-13">
            {{ `${group} group` }}
          </q-item-section>
        </q-item>

        <q-item
          dense
          clickable
          v-for="(taskList, idx) in list"
          :key="idx"
          :group="group"
          :list="taskList.name"
          :active="activeFilters && activeFilters.has(`${group}_${taskList.name}`)"
          class="q-pr-sm"
          active-class="text-weight-bold bg-indigo-1 text-indigo-5"
          @click.stop="filter"
        >
          <q-item-section class="inset-item">
            {{ taskList.name }}
          </q-item-section>

          <q-item-section class="col-grow">
            <div class="row q-ml-sm">
              <q-badge
                rounded
                color="indigo-2"
                class="text-detail text-weight-600 text-indigo-5 q-mx-sm q-my-xs"
                :label="taskList.taskCount"
              />
              <q-btn
                v-if="isAdmin"
                flat
                dense
                size="sm"
                color="grey-6"
                icon="o_edit"
                class="q-ml-auto q-mr-xs strong-focus outlined-item"
                @click.stop="handleEdit(taskList)"
              >
                <TooltipWidget anchor="center left" self="center right" :offset="[10, 10]">
                  Edit task list
                </TooltipWidget>
              </q-btn>

              <q-btn
                v-if="isAdmin"
                flat
                dense
                size="sm"
                :color="taskList.taskCount > 0 ? 'grey-4' : 'grey-6'"
                icon="o_delete"
                class="strong-focus outlined-item"
                :disable="taskList.taskCount > 0"
                @click.stop="handleDelete(taskList)"
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
            </div>
          </q-item-section>
        </q-item>
      </template>

      <q-item
        v-if="isAdmin"
        clickable
        v-close-popup
        dense
        class="text-grey-8"
        @click.stop="handleCreate"
      >
        <q-item-section side class="q-pr-xs">
          <q-icon name="o_playlist_add" size="xs" />
        </q-item-section>
        <q-item-section class="text-weight-600">New Task List</q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
import cuid from "cuid";
import { isNil } from "ramda";
import { computed, defineComponent, inject, ref } from "vue";
import { useRouter } from "vue-router";
import { useActor } from "@xstate/vue";
import { requests } from "@/api";
import forms from "@/forms";
import { useAPI, useEditing, useEventHandling, useStores } from "@/use";
import { TooltipWidget } from "@/components";

export default defineComponent({
  name: "TasklistList",
  components: {
    TooltipWidget,
  },
  emits: ["onReload"],
  setup(_, context) {
    const { apiInterface } = useAPI();
    const {
      editingIndex,
      showEditing,
      modals,
      machine: { send },
    } = useEditing();
    const { notifier } = useEventHandling();
    const { isAdmin } = useStores();
    const $router = useRouter();

    const title = "Task Lists";
    const activeFilters = ref(new Set());
    const taskLists = inject("taskLists");

    const filter = (e) => {
      let group = e.currentTarget.getAttribute("group");
      let list = e.currentTarget.getAttribute("list");

      const { filter } = $router.currentRoute.value.query;
      const prevFilter = filter ? new Set(filter.split(",")) : new Set();
      const clicked = list ? `${group}_${list}` : group;
      prevFilter.has(clicked) ? prevFilter.delete(clicked) : prevFilter.add(clicked);

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
    }

    const handleCreate = () => {
      send("SPAWN_FORM", {
        cuid: cuid(),
        key: null,
        kind: "taskList",
        mode: "create",
        initialData: {},
      });
      showEditing.value();
    };

    const handleEdit = async ({ id }) => {
      const key = `form-taskList-${id}`;
      const indexed = editingIndex.value[key];
      if (!isNil(indexed)) {
        const { send: actorSend } = useActor(modals.value[indexed.cuid].actor);
        send("SET_FOCUS", { value: indexed.cuid });
        actorSend("SHOW");
      } else {
        const { data, success, fetchAPI } = apiInterface();
        const { edit: editSchema } = forms.taskList;
        await fetchAPI(requests.tasks.getTaskList(id));
        if (success.value) {
          await editSchema.validate(data.value, { stripUnknown: true }).then((value) => {
            send("SPAWN_FORM", {
              cuid: cuid(),
              kind: "taskList",
              mode: "update",
              initialData: value,
              key,
            });
            showEditing.value();
          });
        }
      }
    };

    const handleDelete = (taskList) => {
      const { success, fetchAPI } = apiInterface();
      const request = requests.tasks.deleteTaskList(taskList.id);
      fetchAPI(request).then(() => {
        if (success.value) {
          notifier.tasks.taskListDeleted(taskList.name);
          context.emit("onReload");
        }
      });
    };

    const clearActiveFilters = () => {
      activeFilters.value = new Set();
      // const { filter } = $router.currentRoute.value.query;
      const newFilters = Array.from(activeFilters.value).join(",");
      $router.push({
        query: { ...(newFilters && { filter: newFilters }) },
      });
    };

    return {
      activeFilters,
      clearActiveFilters,
      filter,
      handleCreate,
      handleEdit,
      handleDelete,
      isAdmin,
      taskLists,
      title,
    };
  },
});
</script>

<style lang="scss">
.task-list-menu {
  min-width: 300px;
}
.inset-item {
  padding-left: 22px;
}
</style>
