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
            <Tooltip>
              {{ showing ? "Hide task lists" : "Show task lists" }}
            </Tooltip>
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
            <Tooltip> Create Task List </Tooltip>
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
                <Tooltip
                  anchor="center left"
                  self="center right"
                  :offset="[10, 10]"
                >
                  Edit task list
                </Tooltip>
              </q-btn>

              <q-btn
                round
                text-color="black"
                icon="delete"
                size="xs"
                :color="taskList.taskCount === 0 ? 'amber' : 'grey'"
                :disable="taskList.taskCount > 0"
                @click.stop="handleDelete(taskList)"
              >
                <Tooltip
                  v-if="taskList.taskCount === 0"
                  anchor="center left"
                  self="center right"
                  :offset="[10, 10]"
                >
                  Delete task list
                </Tooltip>
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
import { isNil } from "ramda";
import {
  computed,
  defineAsyncComponent,
  defineComponent,
  inject,
  ref,
} from "vue";
import { useRouter } from "vue-router";
import { useActor } from "@xstate/vue";

import { requests } from "@/api";
import forms from "@/forms";
import { useAPI, useEditing, useNotifier, usePermissions } from "@/use";

export default defineComponent({
  name: "TaskLists",
  components: {
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
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
    const $notifier = useNotifier();
    const {
      permissions: { isAdmin },
    } = usePermissions();
    const $router = useRouter();

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
          await editSchema
            .validate(data.value, { stripUnknown: true })
            .then((value) => {
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
}
</style>
