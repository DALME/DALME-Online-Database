<template>
  <q-table
    :columns="columns"
    :filter="filter"
    :no-data-label="noData"
    :pagination="pagination"
    :rows="places"
    :rows-per-page-options="[0]"
    class="sticky-header"
    row-key="id"
    table-colspan="3"
    dense
    flat
    wrap-cells
  >
    <template #body-cell-name="props">
      <q-td :props="props">
        <span v-html="props.value" />
      </q-td>
    </template>
  </q-table>
  <q-separator />
  <MapWidget :places="places" />
</template>

<script>
import { defineComponent, inject, ref } from "vue";

import { MapWidget } from "@/components";
import { getColumns } from "@/utils";

import { columnMap } from "./placeColumns";

export default defineComponent({
  name: "RecordPlaces",
  components: { MapWidget },
  props: {
    places: {
      type: Object,
      required: true,
    },
  },
  setup() {
    const columns = ref(getColumns(columnMap));
    const filter = inject("cardFilter");
    const noData = "No places found.";
    const pagination = { rowsPerPage: 10 }; // 0 = all rows

    return {
      columns,
      filter,
      noData,
      pagination,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-table__top {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding: 0;
}
.q-table__bottom--nodata {
  border: 0;
}
</style>
