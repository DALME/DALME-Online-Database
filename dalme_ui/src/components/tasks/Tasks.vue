<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
        :title="title"
        :rows="filteredRows"
        :columns="columns"
        :visible-columns="visibleColumns"
        :no-data-label="noData"
        :filter="filter"
        :pagination="pagination"
        :title-class="{ 'text-h6': true }"
        row-key="title"
      >
        <template v-slot:top-right>
          <q-input
            borderless
            dense
            debounce="300"
            v-model="filter"
            placeholder="Search"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>

        <template v-slot:body-cell-title="props">
          <q-td class="task" :props="props">
            <router-link
              class="text-subtitle1"
              :to="{ name: 'Task', params: { objId: props.row.id } }"
            >
              {{ props.value }}
            </router-link>
            <div class="details">{{ props.row.description }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-attachments="props">
          <q-td :props="props">
            <q-btn
              push
              @click="openURL(props.value.url)"
              :label="props.value.kind"
              target="_blank"
              color="white"
              size="sm"
              text-color="primary"
              v-if="props.value"
            >
            </q-btn>
          </q-td>
        </template>

        <template v-slot:body-cell-completed="props">
          <q-td :props="props">
            <q-btn
              round
              :color="props.value ? 'green' : 'red'"
              text-color="white"
              :icon="props.value ? 'check_circle_outline' : 'error'"
              size="sm"
            />
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { openURL } from "quasar";
import {
  filter as rFilter,
  flatten,
  has,
  head,
  isEmpty,
  map,
  mapObjIndexed,
  partition,
  keys,
  reverse,
  values,
} from "ramda";
import { defineComponent, inject, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { requests } from "@/api";
import { taskListSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Tasks",
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  async setup(props) {
    const $router = useRouter();
    const $store = useStore();
    const { success, data, fetchAPI } = useAPI();

    const columns = ref([]);
    const visibleColumns = ref([]);
    const rows = ref([]);
    const filteredRows = ref([]);
    const filter = ref("");
    const taskLists = inject("taskLists");

    const noData = "No tasks found.";
    const title = props.embedded ? "My Tasks" : "Tasks";
    const rowsPerPage = props.embedded ? 5 : 20;
    const pagination = { rowsPerPage };

    const getColumns = (keys) => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: {
          id: "ID",
          title: "Task",
          creationTimestamp: "Dates",
          assignedTo: "Assigned to",
          attachments: "Attachments",
          completed: "Status",
        }[key],
        name: key,
        sortable: true,
      });
      return reverse(map(toColumn, keys));
    };

    const filterTasks = (query, taskLists) => {
      let filter = query.filter.split(",");

      const filters = map(
        (taskList) => map((list) => `${list.group}_${list.name}`, taskList),
        taskLists,
      );
      const filterUnion = flatten([keys(filters), values(filters)]);
      filter = rFilter((item) => filterUnion.includes(item), filter);
      $router.push({
        query: isEmpty(filter) ? {} : { filter: filter.join(",") },
      });

      const [groups, lists] = partition((item) => !item.includes("_"), filter);

      let filterSpace = {};
      map((item) => (filterSpace[item] = []), groups);
      map((item) => {
        const [group, list] = item.split("_");
        if (!has(group, filterSpace)) filterSpace[group] = [];
        filterSpace[group].push(list);
      }, lists);

      const filterByGroup = (group) => {
        const sublists = taskLists[group];
        return new Set(
          flatten(map((sublist) => values(sublist.taskIndex), sublists)),
        );
      };

      const filterByLists = (group, lists) =>
        map((list) => filterByList(group, list), lists);

      const filterByList = (group, list) => {
        const sublist = taskLists[group].find((item) => list === item.name);
        return new Set(values(sublist.taskIndex));
      };

      const IDs = mapObjIndexed((lists, group) => {
        return isEmpty(lists)
          ? filterByGroup(group)
          : filterByLists(group, lists);
      }, filterSpace);

      const merged = new Set();
      const mergeIDs = (IDs) => {
        for (const set of values(IDs)) {
          if (Array.isArray(set)) mergeIDs(set);
          for (const item of set) {
            merged.add(item);
          }
        }
      };
      mergeIDs(IDs);

      const final = rFilter((task) => merged.has(task.id), rows.value);
      filteredRows.value = final;
    };

    watch(
      () => $router.currentRoute.value.query,
      (query) => {
        if (isEmpty(query)) {
          filteredRows.value = rows.value;
        } else {
          if (taskLists !== undefined && !isEmpty(taskLists.value)) {
            filterTasks(query, taskLists.value);
          }
        }
      },
    );

    const request = props.embedded
      ? requests.tasks.userTasks($store.getters["auth/userId"])
      : requests.tasks.allTasks();
    await fetchAPI(request);
    if (success.value)
      await taskListSchema
        .validate(data.value, { stripUnknown: true })
        .then((value) => {
          if (!isEmpty(value)) {
            columns.value = getColumns(keys(head(value)));
            visibleColumns.value = map(
              (column) => column.field,
              rFilter(
                (column) =>
                  !["createdBy", "description"].includes(column.field),
                columns.value,
              ),
            );
          }
          rows.value = value;
          const query = $router.currentRoute.value.query;
          taskLists !== undefined &&
          !isEmpty(taskLists.value) &&
          !isEmpty(query)
            ? filterTasks(query, taskLists.value)
            : (filteredRows.value = value);
        });

    return {
      columns,
      filter,
      noData,
      openURL,
      pagination,
      filteredRows,
      title,
      visibleColumns,
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
.task {
  width: 70%;
}
</style>
