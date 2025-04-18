<template>
  <DataTable
    :columns="columns"
    :embedded="embedded"
    :filter-list="filterList"
    :loading="loading"
    :no-data="noData"
    :on-change-filters="onChangeFilters"
    :on-change-page="onChangePage"
    :on-change-rows-per-page="onChangeRowsPerPage"
    :on-change-search="onChangeSearch"
    :on-clear-filters="onClearFilters"
    :on-request="onRequest"
    :pagination="pagination"
    :rows="filteredRows"
    :search="search"
    :sort-list="sortList"
    :title="title"
    :visible-columns="visibleColumns"
    grid
  >
    <template #toolbar-special>
      <TasklistList @on-reload="fetchTaskLists" />
    </template>

    <template #grid-avatar="props">
      <q-icon
        :color="props.row.completed ? 'green-8' : 'red-8'"
        :name="props.row.completed ? 'check_circle_outline' : 'error_outline'"
        size="22px"
      />
    </template>

    <template #grid-main="props">
      <DetailPopover
        :link-target="{ name: 'Task', params: { id: props.row.id } }"
        :link-text="props.row.title"
        link-class="text-h7 title-link"
      >
        <div class="text-detail text-weight-medium text-grey-8 q-mb-sm">
          {{ props.row.creationUser.username }}
          {{ formatDate(props.row.creationTimestamp, "DATETIME_AT") }}
        </div>
        <div class="text-h8 q-mb-xs">{{ props.row.title }}</div>
        <div class="text-detail ellipsis-3-lines">
          {{ props.row.description }}
        </div>
        <div>
          <TagPill
            v-if="props.row.workset"
            :name="`Workset: ${props.row.workset}`"
            class="q-mt-sm"
            colour="light-blue-1"
            module="standalone"
            size="sm"
            text-colour="light-blue-9"
          />
        </div>
      </DetailPopover>
      <TagPill
        v-if="props.row.overdueStatus"
        class="q-ml-sm"
        colour="red-1"
        module="standalone"
        name="overdue"
        size="xs"
        text-colour="red-6"
      />
    </template>

    <template #grid-detail="props">
      <div class="text-detail text-weight-medium text-grey-8">
        <span v-text="`Created on ${formatDate(props.row.creationTimestamp, 'DATETIME_AT')} by `" />
        <!-- <DetailPopover showAvatar :userData="props.row.creationUser" /> -->
        <span
          v-if="props.row.completed && props.row.completedDate"
          v-text="`, completed ${formatDate(props.row.completedDate, 'DATETIME_AT')}`"
        />
      </div>
    </template>

    <template #grid-counter="props">
      <q-icon
        v-if="props.row.commentCount"
        class="text-weight-bold q-mr-xs"
        name="chat_bubble_outline"
        size="17px"
      />
      <div v-if="props.row.commentCount" class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.commentCount }}
      </div>
    </template>

    <template #grid-counter-extra="props">
      <q-btn
        v-if="props.row.file"
        @click.stop="openURL(props.row.file.source)"
        color="blue-gray-6"
        icon="o_text_snippet"
        size="sm"
        target="_blank"
        text-color="blue-gray-6"
        dense
        flat
      />
      <q-btn
        v-if="props.row.url"
        @click.stop="openURL(props.row.url)"
        color="blue-gray-6"
        icon="link"
        size="sm"
        target="_blank"
        text-color="blue-gray-6"
        dense
        flat
      />
    </template>
  </DataTable>
</template>

<script>
import { openURL, useMeta } from "quasar";
import {
  flatten,
  groupBy,
  has,
  isEmpty,
  keys,
  map,
  mapObjIndexed,
  partition,
  filter as rFilter,
  values,
} from "ramda";
import { defineComponent, onMounted, provide, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { requests } from "@/api";
import { DataTable, DetailPopover, TagPill, TasklistList } from "@/components";
import { taskListsSchema, tasksSchema } from "@/schemas";
import { useAPI, useEditing, usePagination, useStores } from "@/use";
import { formatDate, getColumns, getDefaults } from "@/utils";

import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "TaskList",
  components: {
    DetailPopover,
    DataTable,
    TagPill,
    TasklistList,
  },
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["onReloadTaskLists"],
  setup(props, context) {
    if (!props.embedded) useMeta({ title: "Tasks" });
    const $route = useRoute();
    const $router = useRouter();
    const { auth } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const { postSubmitRefreshWatcher } = useEditing();
    const columns = ref([]);
    const rows = ref([]);
    const filteredRows = ref([]);
    const taskLists = ref([]);
    const noData = props.embedded ? "No assigned tasks" : "No tasks found";
    const title = props.embedded ? "My Tasks" : "Tasks";

    // TODO: Move to local useTaskFilter hook and test.
    const filterTasks = (query, taskLists) => {
      let filter = query.filter.split(",");

      const filters = map(
        (taskList) => map((list) => `${list.group.name}_${list.name}`, taskList),
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
        return new Set(flatten(map((sublist) => values(sublist.taskIndex), sublists)));
      };

      const filterByLists = (group, lists) => map((list) => filterByList(group, list), lists);

      const filterByList = (group, list) => {
        const sublist = taskLists[group].find((item) => list === item.name);
        return new Set(values(sublist.taskIndex));
      };

      const IDs = mapObjIndexed((lists, group) => {
        return isEmpty(lists) ? filterByGroup(group) : filterByLists(group, lists);
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
          if (taskLists.value !== undefined && !isEmpty(taskLists.value)) {
            filterTasks(query, taskLists.value);
          }
        }
      },
    );

    const fetchData = async (query) => {
      const request = props.embedded
        ? requests.tasks.getUserTasks(auth.user.userId)
        : requests.tasks.getTasks(query);
      await fetchAPI(request);
      if (success.value)
        await tasksSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
          columns.value = getColumns(columnMap);
          pagination.value.rowsNumber = data.value.count;
          rows.value = value;
          const query = $router.currentRoute.value.query;
          taskLists.value !== undefined && !isEmpty(taskLists.value) && !isEmpty(query)
            ? filterTasks(query, taskLists.value)
            : (filteredRows.value = rows.value);
          loading.value = false;
        });
    };

    const fetchTaskLists = async () => {
      const { success, data, fetchAPI } = apiInterface();
      const request = requests.tasks.getTaskLists();
      fetchAPI(request).then(() => {
        if (success.value)
          taskListsSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
            const grouped = groupBy((tasklist) => tasklist.teamLink.name, value);
            taskLists.value = grouped;
          });
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
    } = usePagination(fetchData, $route.name, getDefaults(columnMap), props.embedded);

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);
    provide("taskLists", taskLists);

    postSubmitRefreshWatcher(fetchTaskLists);
    onMounted(async () => await fetchTaskLists());

    return {
      context,
      columns,
      filteredRows,
      filterList: filterList(auth.user.userId),
      formatDate,
      fetchTaskLists,
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
      sortList: sortList(),
      title,
      visibleColumns,
    };
  },
});
</script>
