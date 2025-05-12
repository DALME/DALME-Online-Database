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
    <template #render-cell-country="props">
      <router-link
        v-if="props.row.country"
        :to="{ name: 'Countries', params: { id: props.row.country.id } }"
        class="text-link"
      >
        {{ props.row.country.name }}
      </router-link>
    </template>
  </DataTable>
</template>

<script>
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { DataTable } from "@/components";
import { localeListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { getColumns, getDefaults } from "@/utils";

import { columnMap } from "./columns";

export default defineComponent({
  name: "LocaleList",
  components: {
    DataTable,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No locales found.";
    const title = "Locales";

    const fetchData = async (query) => {
      const request = requests.locales.list(query);
      await fetchAPI(request);
      if (success.value)
        await localeListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
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
      search,
      rows,
      title,
      visibleColumns,
      schema: localeListSchema,
    };
  },
});
</script>
