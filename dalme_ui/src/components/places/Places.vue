<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
        :title="title"
        :rows="rows"
        :columns="columns"
        :visible-columns="visibleColumns"
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

        <template v-slot:body-cell-locale="props">
          <q-td :props="props">
            <template v-if="props.value">
              {{ getLocale(props.value) }}
            </template>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { filter as rFilter, head, isEmpty, map, keys } from "ramda";
import { defineComponent, ref } from "vue";

import { requests } from "@/api";
import { useAPI } from "@/use";
import { placeListSchema } from "@/schemas";

export default defineComponent({
  name: "Places",
  async setup(_, context) {
    const { success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const visibleColumns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No places found.";
    const title = "Places";
    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

    const getColumns = (keys) => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: {
          id: "ID",
          standardName: "Standard Name",
          notes: "Notes",
          locale: "Locale",
        }[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys);
    };

    const getLocale = (value) =>
      `${value.name}, ${value.administrativeRegion}, ${value.country}`;

    const fetchData = async () => {
      const request = requests.places.getPlaces();
      await fetchAPI(request);
      if (success.value)
        await placeListSchema
          .validate(data.value, { stripUnknown: true })
          .then(async (value) => {
            if (!isEmpty(value)) {
              columns.value = getColumns(keys(head(value)));
            }
            visibleColumns.value = map(
              (column) => column.field,
              rFilter(
                (column) => !["id"].includes(column.field),
                columns.value,
              ),
            );
            rows.value = value;
          });
    };

    await fetchData();

    return {
      columns,
      filter,
      getLocale,
      noData,
      pagination,
      rows,
      title,
      visibleColumns,
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
</style>
