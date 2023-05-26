<template>
  <DataTable
    :columns="columns"
    :editable="editable"
    :search="search"
    :loading="loading"
    :noData="noData"
    :onChangeSearch="onChangeSearch"
    :onChangePage="onChangePage"
    :onChangeRowsPerPage="onChangeRowsPerPage"
    :onRequest="onRequest"
    :pagination="pagination"
    :rows="rows"
    :schema="schema"
    :title="title"
    :updateRequest="updateRequest"
    :visibleColumns="visibleColumns"
  >
    <template v-slot:render-cell-locale="props">
      <router-link
        class="text-link"
        v-if="props.row.locale"
        :to="{ name: 'Locales', params: { id: props.row.locale.id } }"
      >
        {{ props.row.locale.name }}
      </router-link>
    </template>
  </DataTable>
</template>

<script>
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { DataTable } from "@/components";
import { getColumns, getDefaults } from "@/components/utils";
import { placeListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { columnMap } from "./columns";

export default defineComponent({
  name: "PlaceList",
  components: {
    DataTable,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No places found.";
    const title = "Places";

    const updateRequest = requests.places.inlineUpdate;
    const editable = ["notes"];

    const fetchData = async (query) => {
      const request = requests.places.getPlaces(query);
      await fetchAPI(request);
      if (success.value)
        await placeListSchema
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
      editable,
      loading,
      noData,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      pagination,
      rows,
      schema: placeListSchema,
      search,
      title,
      updateRequest,
      visibleColumns,
    };
  },
});
</script>
