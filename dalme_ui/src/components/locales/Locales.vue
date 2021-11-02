<template>
  <div class="q-ma-md full-width full-height">
    <Table
      :title="title"
      :columns="columns"
      :loading="loading"
      :filter="filter"
      :editable="editable"
      :schema="schema"
      :no-data-label="noData"
      :fetch-data="fetchData"
      :update-request="request"
    />
  </div>
</template>

<script>
import { map, keys } from "ramda";
import { defineComponent, onMounted, provide, ref } from "vue";

import { requests } from "@/api";
import { Table } from "@/components";
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
    Table,
  },
  setup(_, context) {
    const { loading, success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No locales found.";
    const title = "Locales";
    const request = requests.locales.updateLocales;
    const editable = ["name", "longitude", "latitude"];

    provide("rows", rows);

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
      editable,
      filter,
      loading,
      noData,
      rows,
      title,
      request,
      fetchData,
      schema: localeListSchema,
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
.dirty {
  border: 2px solid #f44336;
}
</style>
