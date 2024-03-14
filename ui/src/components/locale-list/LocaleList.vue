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
    <template v-slot:render-cell-country="props">
      <router-link
        v-if="props.row.country"
        class="text-link"
        :to="{ name: 'Countries', params: { id: props.row.country.id } }"
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
import { getColumns, getDefaults } from "@/utils";
import { localeListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
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
      const request = requests.locales.getLocales(query);
      await fetchAPI(request);
      if (success.value)
        await localeListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
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
      search,
      rows,
      title,
      visibleColumns,
      schema: localeListSchema,
    };
  },
});
</script>
