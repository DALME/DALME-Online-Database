<template>
  <DataTable
    :columns="columns"
    :loading="loading"
    :no-data="noData"
    :on-change-page="onChangePage"
    :on-change-rows-per-page="onChangeRowsPerPage"
    :on-change-search="onChangeSearch"
    :on-request="onRequest"
    :pagination="pagination"
    :rows="rows"
    :search="search"
    :title="title"
    :visible-columns="visibleColumns"
  >
    <template #render-cell-standardName="props">
      <span v-html="props.row.name"></span>
    </template>

    <template #render-cell-type="props">
      {{ props.row.agentType }}
    </template>
  </DataTable>
</template>

<script>
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { DataTable } from "@/components";
import { agentListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { getColumns, getDefaults } from "@/utils";

import { columnMap } from "./columns";

export default defineComponent({
  name: "AgentList",
  components: {
    DataTable,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No agents found.";
    const title = "Agents";

    const fetchData = async (query) => {
      const request = requests.agents.getAgents(query);
      await fetchAPI(request);
      if (success.value)
        await agentListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
          columns.value = getColumns(columnMap);
          pagination.value.rowsNumber = data.value.count;
          rows.value = value;
          loading.value = false;
        });
    };

    const {
      fetchDataPaginated,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      pagination,
      search,
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap));

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);

    return {
      columns,
      loading,
      noData,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      pagination,
      rows,
      search,
      title,
      visibleColumns,
    };
  },
});
</script>
