<template>
  <DataTable
    :columns="columns"
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
    :rows="rows"
    :title="title"
    :visibleColumns="visibleColumns"
  >
    <template v-slot:render-cell-type="props">
      <span v-text="props.row.isDialect ? 'Dialect' : 'Language'"></span>
    </template>

    <template v-slot:render-cell-parent="props">
      <template v-if="props.row.parent">
        {{ props.row.parent.name }}
      </template>
    </template>
  </DataTable>
</template>

<script>
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { DataTable } from "@/components";
import { getColumns, getDefaults } from "@/utils";
import { languageListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { columnMap } from "./columns";
import { filterList } from "./filters";

export default defineComponent({
  name: "LanguageList",
  components: {
    DataTable,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No languages found.";
    const title = "Languages";

    const fetchData = async (query) => {
      const request = requests.languages.getLanguages(query);
      await fetchAPI(request);
      if (success.value)
        await languageListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
          columns.value = getColumns(columnMap);
          pagination.value.rowsNumber = data.value.count;
          rows.value = value;
          loading.value = false;
        });
    };

    const {
      activeFilters,
      fetchDataPaginated,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      onRequest,
      pagination,
      search,
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap));

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);

    return {
      columns,
      loading,
      noData,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      onRequest,
      pagination,
      search,
      rows,
      title,
      visibleColumns,
      filterList,
    };
  },
});
</script>
