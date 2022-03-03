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
        :loading="loading"
        row-key="title"
      >
        <template v-if="showSearch" v-slot:top-right>
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

        <template v-slot:no-data="{ message }">
          <div>{{ message }}</div>
        </template>

        <template v-slot:body-cell-title="props">
          <q-td class="task" :props="props">
            <router-link
              class="text-subtitle1"
              :to="{ name: 'Task', params: { id: props.row.id } }"
            >
              {{ props.value }}
            </router-link>
            <div>{{ props.row.description }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-attachments="props">
          <q-td :props="props"> </q-td>
        </template>

        <template v-slot:body-cell-completed="props">
          <q-td :props="props">
            <q-btn
              round
              :color="props.value ? 'green' : 'red'"
              text-color="white"
              :icon="props.value ? 'check_circle_outline' : 'error'"
              size="xs"
            />
          </q-td>
        </template>
      </q-table>
    </q-card>
    <OpaqueSpinner :showing="loading" />
  </div>
</template>

<script>
import { openURL } from "quasar";
import {
  filter as rFilter,
  flatten,
  has,
  isEmpty,
  map,
  mapObjIndexed,
  partition,
  keys,
  values,
} from "ramda";
import { defineComponent, inject, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
import { tasksSchema } from "@/schemas";
import { useAPI } from "@/use";

const columnMap = {
  id: "ID",
  completed: "Status",
  title: "Task",
  assignedTo: "Assigned to",
  attachments: "Attachments",
  owner: "Owner",
  creationTimestamp: "Dates",
};

export default defineComponent({
  name: "Tasks",
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    OpaqueSpinner,
  },
  setup(props, context) {
    const $router = useRouter();
    const $store = useStore();
    const { loading, success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const visibleColumns = ref(null);
    const rows = ref([]);
    const filteredRows = ref([]);
    const filter = ref("");
    const taskLists = props.embedded ? ref([]) : inject("taskLists");
    const showSearch = ref(true);

    const noData = props.embedded ? "No assigned tasks." : "No tasks found.";
    const title = props.embedded ? "My Tasks" : "Tasks";
    const rowsPerPage = props.embedded ? 5 : 25;
    const pagination = { rowsPerPage };

    const getColumns = () => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys(columnMap));
    };

    // TODO: Move to local useTaskFilter hook.
    const filterTasks = (query, taskLists) => {
      let filter = query.filter.split(",");

      const filters = map(
        (taskList) =>
          map((list) => `${list.group.name}_${list.name}`, taskList),
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

    const setColumns = () => {
      columns.value = getColumns();
      const excluded = props.embedded
        ? ["owner", "description", "createdBy"]
        : ["description", "createdBy"];
      visibleColumns.value = map(
        (column) => column.field,
        rFilter((column) => !excluded.includes(column.field), columns.value),
      );
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

    const fetchData = async () => {
      const request = props.embedded
        ? requests.tasks.getUserTasks($store.getters["auth/userId"])
        : requests.tasks.getTasks();
      await fetchAPI(request);
      if (success.value)
        await tasksSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            if (isEmpty(value)) {
              if (props.embedded) showSearch.value = false;
            } else {
              setColumns();
            }
            rows.value = value;
            const query = $router.currentRoute.value.query;
            taskLists !== undefined &&
            !isEmpty(taskLists.value) &&
            !isEmpty(query)
              ? filterTasks(query, taskLists.value)
              : (filteredRows.value = value);
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    return {
      columns,
      filter,
      filteredRows,
      loading,
      noData,
      openURL,
      pagination,
      showSearch,
      title,
      visibleColumns,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-table tbody td {
  white-space: normal;
}
.task {
  width: 70%;
}
</style>
