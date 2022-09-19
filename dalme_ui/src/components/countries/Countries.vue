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
  />
</template>

<script>
import { defineComponent, onMounted, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import BasicTable from "@/components/basic-table/BasicTable.vue";
import { getColumns, getDefaults } from "@/components/utils";
import { countryListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";

const columnMap = {
  name: {
    label: "Name",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: true,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
  alpha2Code: {
    label: "Alpha 2 Code",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
    autoWidth: true,
  },
  alpha3Code: {
    label: "Alpha 3 Code",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
    autoWidth: true,
  },
  numCode: {
    label: "Numeric Code",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
    autoWidth: true,
  },
};

export default defineComponent({
  name: "Countries",
  components: {
    BasicTable,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No countries found.";
    const title = "Countries";

    const fetchData = async () => {
      const request = requests.countries.getCountries();
      await fetchAPI(request);
      if (success.value)
        await countryListSchema
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
