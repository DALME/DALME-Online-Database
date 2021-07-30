<template>
  <q-table
    :rows="rows"
    :columns="columns"
    :visible-columns="visibleColumns"
    :no-data-label="noData"
    :filter="filter"
    :pagination="pagination"
    :rows-per-page-options="[0]"
    row-key="id"
  >
    <template v-slot:top>
      <q-item-section avatar>
        <q-avatar>
          <q-icon name="menu_book" />
        </q-avatar>
      </q-item-section>
      <q-item-label class="text-weight-medium">
        Places ({{ places.length }})
      </q-item-label>
      <q-space />
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
  </q-table>
</template>

<script>
import { filter as rFilter, keys, map } from "ramda";
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "SourcePlaces",
  props: {
    places: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const columns = ref([]);
    const visibleColumns = ref([]);
    const filter = ref("");

    const noData = "No places found.";
    const pagination = { rowsPerPage: 0 }; // All rows.

    const getColumns = (keys) => {
      const columnMap = {
        placename: "Placename",
        locale: "Locale",
      };
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys);
    };
    columns.value = getColumns(keys(props.places[0]));
    visibleColumns.value = map(
      (column) => column.field,
      rFilter((column) => !["objId"].includes(column.field), columns.value),
    );

    return {
      columns,
      visibleColumns,
      filter,
      noData,
      pagination,
      rows: props.places,
    };
  },
});
</script>

<style lang="scss">
.q-table__top {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding-top: 8px;
  padding-bottom: 8px;
}
.q-table__bottom--nodata {
  border: 0;
}
</style>
