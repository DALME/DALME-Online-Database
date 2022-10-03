<template>
  <Table
    grid
    :columns="columns"
    :embedded="embedded"
    :search="search"
    :filterList="filterList"
    :loading="loading"
    :noData="noData"
    :onChangeSearch="onChangeSearch"
    :onChangePage="onChangePage"
    :onChangeRowsPerPage="onChangeRowsPerPage"
    :onChangeFilters="onChangeFilters"
    :onClearFilters="onClearFilters"
    :onRequest="onRequest"
    :pagination="pagination"
    :rows="filteredRows"
    :sortList="sortList"
    :title="title"
    :visibleColumns="visibleColumns"
  >
    <template v-slot:toolbar-special>
      <TaskLists @on-reload="context.emit('onReloadTaskLists')" />
    </template>

    <template v-slot:grid-avatar="props">
      <q-icon
        :name="props.row.completed ? 'check_circle_outline' : 'error_outline'"
        :color="props.row.completed ? 'green-8' : 'red-8'"
        size="22px"
      />
    </template>

    <template v-slot:grid-main="props">
      <DetailPopover
        linkClass="text-h7 title-link"
        :linkTarget="{ name: 'Task', params: { id: props.row.id } }"
        :linkText="props.row.title"
      >
        <div class="text-detail text-weight-medium text-grey-8 q-mb-sm">
          {{ props.row.creationUser.username }}
          {{ formatDate(props.row.creationTimestamp, false) }}
        </div>
        <div class="text-h8 q-mb-xs">{{ props.row.title }}</div>
        <div class="text-detail ellipsis-3-lines">
          {{ props.row.description }}
        </div>
        <div>
          <Tag
            v-if="props.row.workset"
            :name="`Workset: ${props.row.workset}`"
            colour="light-blue-1"
            textColour="light-blue-9"
            size="sm"
            module="standalone"
            class="q-mt-sm"
          />
        </div>
      </DetailPopover>
      <Tag
        v-if="props.row.overdueStatus"
        name="overdue"
        colour="red-1"
        textColour="red-6"
        size="xs"
        module="standalone"
        class="q-ml-sm"
      />
    </template>

    <template v-slot:grid-detail="props">
      <div class="text-detail text-weight-medium text-grey-8">
        <span
          v-text="
            `Created ${formatDate(props.row.creationTimestamp, false)} by `
          "
        />
        <DetailPopover showAvatar :userData="props.row.creationUser" />
        <span
          v-if="props.row.completed && props.row.completedDate"
          v-text="`, completed ${formatDate(props.row.completedDate, false)}`"
        />
      </div>
    </template>

    <template v-slot:grid-counter="props">
      <q-icon
        v-if="props.row.commentCount"
        name="chat_bubble_outline"
        size="17px"
        class="text-weight-bold q-mr-xs"
      />
      <div
        v-if="props.row.commentCount"
        class="text-grey-8 text-weight-bold text-detail"
      >
        {{ props.row.commentCount }}
      </div>
    </template>

    <template v-slot:grid-counter-extra="props">
      <q-btn
        v-if="props.row.file"
        flat
        dense
        @click.stop="openURL(props.row.file.source)"
        target="_blank"
        color="blue-gray-6"
        size="sm"
        icon="o_text_snippet"
        text-color="blue-gray-6"
      />
      <q-btn
        v-if="props.row.url"
        flat
        dense
        @click.stop="openURL(props.row.url)"
        target="_blank"
        color="blue-gray-6"
        size="sm"
        icon="link"
        text-color="blue-gray-6"
      />
    </template>
  </Table>
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
import { defineComponent, inject, provide, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { requests } from "@/api";
import { Table, TaskLists } from "@/components";
import {
  DetailPopover,
  formatDate,
  getColumns,
  getDefaults,
  Tag,
} from "@/components/utils";
import { tasksSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "Tasks",
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    DetailPopover,
    Table,
    Tag,
    TaskLists,
  },
  emits: ["onReloadTaskLists"],
  setup(props, context) {
    const $route = useRoute();
    const $router = useRouter();
    const $authStore = useAuthStore();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const filteredRows = ref([]);
    const taskLists = props.embedded ? ref([]) : inject("taskLists");
    const noData = props.embedded ? "No assigned tasks" : "No tasks found";
    const title = props.embedded ? "My Tasks" : "Tasks";

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

    const fetchData = async (query) => {
      const request = props.embedded
        ? requests.tasks.getUserTasks($authStore.userId)
        : requests.tasks.getTasks(query);
      await fetchAPI(request);
      if (success.value)
        await tasksSchema
          .validate(data.value.data, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns(columnMap);
            pagination.value.rowsNumber = data.value.recordsFiltered;
            pagination.value.rowsTotal = data.value.recordsTotal;
            rows.value = value;
            const query = $router.currentRoute.value.query;
            taskLists !== undefined &&
            !isEmpty(taskLists.value) &&
            !isEmpty(query)
              ? filterTasks(query, taskLists.value)
              : (filteredRows.value = rows.value);
            loading.value = false;
          });
    };

    const {
      activeFilters,
      fetchDataPaginated,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      onChangeFilters,
      onClearFilters,
      pagination,
      search,
      visibleColumns,
    } = usePagination(
      fetchData,
      $route.name,
      getDefaults(columnMap),
      props.embedded,
    );

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);

    return {
      context,
      columns,
      filteredRows,
      filterList,
      formatDate,
      loading,
      noData,
      openURL,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      onRequest,
      pagination,
      rows,
      search,
      sortList,
      title,
      visibleColumns,
    };
  },
});
</script>
