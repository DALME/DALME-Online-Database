<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
        :title="title"
        :rows="rows"
        :columns="columns"
        :no-data-label="noData"
        :filter="filter"
        :pagination="pagination"
        :title-class="{ 'text-h6': true }"
        :loading="loading"
        row-key="id"
      >
        <template v-slot:top-right>
          <q-input
            borderless
            dense
            debounce="300"
            v-model="filter"
            placeholder="Search"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>

        <template v-slot:body-cell-locale="props">
          <q-td :props="props">
            <template v-if="props.value">
              {{ getLocale(props.value) }}
            </template>
          </q-td>
        </template>
      </q-table>
    </q-card>
    <OpaqueSpinner :showing="loading" />
  </div>
</template>

<script>
import { map, keys } from "ramda";
import { defineComponent, onMounted, ref } from "vue";

import { requests } from "@/api";
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
  },
  setup() {
    const { apiInterface } = useAPI();

    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No places found.";
    const title = "Places";
    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

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

    const getLocale = (value) =>
      `${value.name}, ${value.administrativeRegion}, ${value.country}`;

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
      filter,
      getLocale,
      loading,
      noData,
      pagination,
      rows,
      title,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-table tbody td {
  white-space: normal;
}
</style>
