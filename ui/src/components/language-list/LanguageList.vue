<template>
  <DataTable
    :columns="columns"
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
    :rows="rows"
    :search="search"
    :title="title"
    :visible-columns="visibleColumns"
  >
    <template #render-cell-type="props">
      <span v-text="props.row.isDialect ? 'Dialect' : 'Language'"></span>
    </template>

    <template #render-cell-parent="props">
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
import { languageListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { getColumns, getDefaults } from "@/utils";

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
