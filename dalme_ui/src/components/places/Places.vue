<template>
  <BasicTable
    :columns="columns"
    :editable="editable"
    :filter="filter"
    :loading="loading"
    :noData="noData"
    :onChangeFilter="onChangeFilter"
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
  </BasicTable>
</template>

<script>
import { defineComponent, onMounted, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import BasicTable from "@/components/basic-table/BasicTable.vue";
import { getColumns, getDefaults } from "@/components/utils";
import { placeListSchema } from "@/schemas";
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
  notes: {
    label: "Notes",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
    classes: null,
    headerClasses: "text-no-wrap",
    isDefaultVisible: true,
  },
  locale: {
    label: "Locale",
    align: "left",
    sortable: true,
    sortOrder: "ad",
    isSortDefault: false,
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
};

export default defineComponent({
  name: "Places",
  components: {
    BasicTable,
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

    const fetchData = async () => {
      const request = requests.places.getPlaces();
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
      editable,
      filter,
      loading,
      noData,
      onChangeFilter,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      pagination,
      rows,
      schema: placeListSchema,
      title,
      updateRequest,
      visibleColumns,
    };
  },
});
</script>
