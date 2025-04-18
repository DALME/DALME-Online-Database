<template>
  <q-btn-dropdown
    class="bg-indigo-1 text-indigo-9 table-toolbar-button"
    content-class="menu-shadow"
    label="Task Lists"
    menu-anchor="bottom left"
    menu-self="top left"
    size="12px"
    no-caps
    unelevated
  >
    <q-list class="text-grey-9 task-list-menu" bordered separator>
      <q-item class="q-pr-sm" dense>
        <q-item-section class="text-weight-bold">Task lists</q-item-section>
        <q-item-section avatar>
          <q-btn @click="clearActiveFilters" color="grey-6" icon="close" size="xs" dense flat />
        </q-item-section>
      </q-item>

      <template v-for="(list, group, idx) in taskLists" :key="idx">
        <q-item
          @click.stop="filter"
          :class="
            activeFilters && activeFilters.has(group)
              ? 'text-weight-bold bg-indigo-1 text-indigo-5'
              : 'text-weight-600 text-grey-7'
          "
          :group="group"
          clickable
          dense
        >
          <q-item-section class="q-pr-xs" side>
            <q-icon name="o_group" size="xs" />
          </q-item-section>
          <q-item-section class="text-13">
            {{ `${group} group` }}
          </q-item-section>
        </q-item>

        <q-item
          v-for="(taskList, idx2) in list"
          :key="idx2"
          @click.stop="filter"
          :active="activeFilters && activeFilters.has(`${group}_${taskList.name}`)"
          :group="group"
          :list="taskList.name"
          active-class="text-weight-bold bg-indigo-1 text-indigo-5"
          class="q-pr-sm"
          clickable
          dense
        >
          <q-item-section class="inset-item">
            {{ taskList.name }}
          </q-item-section>

          <q-item-section class="col-grow">
            <div class="row q-ml-sm">
              <q-badge
                :label="taskList.taskCount"
                class="text-detail text-weight-600 text-indigo-5 q-mx-sm q-my-xs"
                color="indigo-2"
                rounded
              />
              <q-btn
                v-if="isAdmin"
                @click.stop="handleEdit(taskList)"
                class="q-ml-auto q-mr-xs strong-focus outlined-item"
                color="grey-6"
                icon="o_edit"
                size="sm"
                dense
                flat
              >
                <ToolTip :offset="[10, 10]" anchor="center left" self="center right">
                  Edit task list
                </ToolTip>
              </q-btn>

              <q-btn
                v-if="isAdmin"
                @click.stop="handleDelete(taskList)"
                :color="taskList.taskCount > 0 ? 'grey-4' : 'grey-6'"
                :disable="taskList.taskCount > 0"
                class="strong-focus outlined-item"
                icon="o_delete"
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
            </div>
          </q-item-section>
        </q-item>
      </template>

      <q-item
        v-if="isAdmin"
        v-close-popup
        @click.stop="handleCreate"
        class="text-grey-8"
        clickable
        dense
      >
        <q-item-section class="q-pr-xs" side>
          <q-icon name="o_playlist_add" size="xs" />
        </q-item-section>
        <q-item-section class="text-weight-600">New Task List</q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
import { createId as cuid } from "@paralleldrive/cuid2";
import { useActor } from "@xstate/vue";
import { isNil } from "ramda";
import { computed, defineComponent, inject, ref } from "vue";
import { useRouter } from "vue-router";

import { requests } from "@/api";
import { ToolTip } from "@/components";
import forms from "@/forms";
import { useAPI, useEditing, useEventHandling, useStores } from "@/use";

export default defineComponent({
  name: "TasklistList",
  components: {
    ToolTip,
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
    const { auth } = useStores();
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
      send({
        type: "SPAWN_FORM",
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
        send({ type: "SET_FOCUS", value: indexed.cuid });
        actorSend({ type: "SHOW" });
      } else {
        const { data, success, fetchAPI } = apiInterface();
        const { edit: editSchema } = forms.taskList;
        await fetchAPI(requests.tasks.getTaskList(id));
        if (success.value) {
          await editSchema.validate(data.value, { stripUnknown: true }).then((value) => {
            send({
              type: "SPAWN_FORM",
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
      isAdmin: auth.user.isAdmin,
      taskLists,
      title,
    };
  },
});
</script>

<style lang="scss" scoped>
.task-list-menu {
  min-width: 300px;
}
.inset-item {
  padding-left: 22px;
}
</style>
