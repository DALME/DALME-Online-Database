<template>
  <div class="q-ma-md full-width full-height">
    <Table
      :title="title"
      :columns="columns"
      :loading="loading"
      :filter="filter"
      :schema="schema"
      :no-data-label="noData"
      :fetch-data="fetchData"
    />
    <OpaqueSpinner :showing="loading" />
  </div>
</template>

<script>
import { map, keys } from "ramda";
import { defineComponent, onMounted, provide, ref } from "vue";

import { requests } from "@/api";
import { Table } from "@/components";
import { OpaqueSpinner } from "@/components/utils";
import { localeListSchema } from "@/schemas";
import { useAPI } from "@/use";

const columnMap = {
  name: "Name",
  administrativeRegion: "Administrative Region",
  country: "Country",
  latitude: "Latitude",
  longitude: "Longitude",
};

export default defineComponent({
  name: "Locales",
  components: {
    OpaqueSpinner,
    Table,
  },
  setup() {
    const { apiInterface } = useAPI();

    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    provide("rows", rows);

    const noData = "No locales found.";
    const title = "Locales";

    const getColumns = () => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys(columnMap));
    };

    const fetchData = async () => {
      const request = requests.locales.getLocales();
      await fetchAPI(request);
      if (success.value)
        await localeListSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns();
            rows.value = value;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    return {
      columns,
      filter,
      loading,
      noData,
      title,
      fetchData,
      schema: localeListSchema,
    };
  },
});
</script>
