<template>
  <div class="q-ma-md full-width full-height">
    <Table
      :title="title"
      :columns="columns"
      :editable="editable"
      :loading="loading"
      :filter="filter"
      :schema="schema"
      :no-data-label="noData"
      :fetch-data="fetchData"
      :updateRequest="updateRequest"
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
import { useAPI } from "@/use";
import { placeListSchema } from "@/schemas";

const columnMap = {
  standardName: "Standard Name",
  notes: "Notes",
  locale: "Locale",
};

export default defineComponent({
  name: "Places",
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

    const updateRequest = requests.places.inlineUpdate;
    const editable = ["notes"];

    provide("rows", rows);

    const noData = "No places found.";
    const title = "Places";

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
      const request = requests.places.getPlaces();
      await fetchAPI(request);
      if (success.value)
        await placeListSchema
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
      fetchData,
      filter,
      loading,
      noData,
      title,
      updateRequest,
      schema: placeListSchema,
    };
  },
});
</script>
