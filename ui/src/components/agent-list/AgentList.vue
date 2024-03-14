<template>
  <DataTable
    :columns="columns"
    :search="search"
    :loading="loading"
    :noData="noData"
    :onChangeSearch="onChangeSearch"
    :onChangePage="onChangePage"
    :onChangeRowsPerPage="onChangeRowsPerPage"
    :onRequest="onRequest"
    :pagination="pagination"
    :rows="rows"
    :title="title"
    :visibleColumns="visibleColumns"
  >
    <template v-slot:render-cell-standardName="props">
      <span v-html="props.row.standardName"></span>
    </template>

    <template v-slot:render-cell-type="props">
      {{ props.row.type.name }}
    </template>
  </DataTable>
</template>

<script>
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { DataTable } from "@/components";
import { getColumns, getDefaults } from "@/utils";
import { agentListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
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
          pagination.value.rowsNumber = data.value.filtered;
          pagination.value.rowsTotal = data.value.count;
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
