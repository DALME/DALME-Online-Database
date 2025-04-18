<template>
  <DataTable
    :columns="columns"
    :editable="editable"
    :loading="loading"
    :no-data="noData"
    :on-change-page="onChangePage"
    :on-change-rows-per-page="onChangeRowsPerPage"
    :on-change-search="onChangeSearch"
    :on-request="onRequest"
    :pagination="pagination"
    :rows="rows"
    :schema="schema"
    :search="search"
    :title="title"
    :update-request="updateRequest"
    :visible-columns="visibleColumns"
  >
    <template #render-cell-locale="props">
      <router-link
        v-if="props.row.locale"
        :to="{ name: 'Locales', params: { id: props.row.locale.id } }"
        class="text-link"
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
import { placeListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { getColumns, getDefaults } from "@/utils";

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

    const getLocationDetail = (place) => {
      if (!place.location) return null;
      if (place.location.locationType == "Locale") {
        const name = place.location?.attributes[0]?.value.name;
        const region = place.location?.attributes[0]?.value.administrativeRegion;
        const country = place.location?.attributes[0]?.value.country?.name;
        return `${name}, ${region} (${country})`;
      }
    };

    const fetchData = async (query) => {
      const request = requests.places.getPlaces(query);
      await fetchAPI(request);
      if (success.value)
        await placeListSchema.validate(data.value.data, { stripUnknown: false }).then((value) => {
          columns.value = getColumns(columnMap);
          pagination.value.rowsNumber = data.value.count;
          value.forEach((p) => {
            p.locationType = p.location?.locationType || null;
            p.locationDetail = getLocationDetail(p);
          });
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
