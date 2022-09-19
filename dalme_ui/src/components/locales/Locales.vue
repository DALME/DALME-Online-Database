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
    <template v-slot:render-cell-country="props">
      <router-link
        v-if="props.row.country"
        class="text-link"
        :to="{ name: 'Countries', params: { id: props.row.country.id } }"
      >
        {{ props.row.country.name }}
      </router-link>
    </template>
  </BasicTable>
</template>

<script>
import { defineComponent, onMounted, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import BasicTable from "@/components/basic-table/BasicTable.vue";
import { getColumns, getDefaults } from "@/components/utils";
import { localeListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";

const columnMap = {
  name: {
    label: "Standard Name",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: true,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
  administrativeRegion: {
    label: "Administrative Region",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
  country: {
    label: "Country",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
  latitude: {
    label: "Latitude",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
  longitude: {
    label: "Longitude",
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
  name: "Locales",
  components: {
    BasicTable,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No locales found.";
    const title = "Locales";

    const fetchData = async () => {
      const request = requests.locales.getLocales();
      await fetchAPI(request);
      if (success.value)
        await localeListSchema
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
      schema: localeListSchema,
    };
  },
});
</script>
