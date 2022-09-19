<template>
  <BasicTable
    :columns="columns"
    :filter="filter"
    :loading="loading"
    :noData="noData"
    :onChangeFilter="onChangeFilter"
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
  </BasicTable>
</template>

<script>
import { defineComponent, onMounted, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import BasicTable from "@/components/basic-table/BasicTable.vue";
import { getColumns, getDefaults } from "@/components/utils";
import { agentListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";

const columnMap = {
  standardName: {
    label: "Standard Name",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: true,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
  type: {
    label: "Type",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
  user: {
    label: "User",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
};

export default defineComponent({
  name: "Agents",
  components: {
    BasicTable,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No agents found.";
    const title = "Agents";

    const fetchData = async () => {
      const request = requests.agents.getAgents();
      await fetchAPI(request);
      if (success.value)
        await agentListSchema
          .validate(data.value.data, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns(columnMap);
            pagination.value.rowsNumber = data.value.recordsFiltered;
            pagination.value.rowsTotal = data.value.recordsTotal;
            rows.value = value;
            loading.value = false;
          });
    };

    const {
      fetchDataPaginated,
      filter,
      onChangeFilter,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      pagination,
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap));

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);

    onMounted(async () => await fetchData());

    return {
      columns,
      filter,
      loading,
      noData,
      onChangeFilter,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      pagination,
      rows,
      title,
      visibleColumns,
    };
  },
});
</script>
