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

        <template v-slot:body-cell-country="props">
          <q-td :props="props">
            {{ props.value.name }}
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { map, keys } from "ramda";
import { defineComponent, ref } from "vue";

import { requests } from "@/api";
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
  async setup(_, context) {
    const { success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No locales found.";
    const title = "Locales";
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

    const fetchData = async () => {
      const request = requests.locales.getLocales();
      await fetchAPI(request);
      if (success.value)
        await localeListSchema
          .validate(data.value, { stripUnknown: true })
          .then(async (value) => {
            columns.value = getColumns();
            rows.value = value;
          });
    };

    await fetchData();

    return {
      columns,
      filter,
      noData,
      pagination,
      rows,
      title,
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
</style>
