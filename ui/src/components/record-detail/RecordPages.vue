<template>
  <q-table
    :columns="columns"
    :filter="filter"
    :no-data-label="noData"
    :pagination="pagination"
    :rows="pages"
    :rows-per-page-options="[0]"
    class="sticky-header"
    row-key="id"
    table-colspan="5"
    dense
    flat
    wrap-cells
  >
    <template #body-cell-hasImage="props">
      <q-td :props="props"><BooleanValue :value="props.value" /></q-td>
    </template>

    <template #body-cell-hasTranscription="props">
      <q-td :props="props"><BooleanValue :value="props.value" /></q-td>
    </template>
  </q-table>
</template>

<script>
import { defineComponent, inject } from "vue";

import { BooleanValue } from "@/components";

export default defineComponent({
  name: "RecordPages",
  components: {
    BooleanValue,
  },
  props: {
    pages: {
      type: Array,
      required: true,
    },
  },
  setup() {
    const columns = inject("pageColumns");
    const filter = inject("cardFilter");
    const noData = "No folios found.";
    const pagination = { rowsPerPage: 0 }; // All rows.

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
  padding-top: 8px;
  padding-bottom: 8px;
}
.q-table__bottom--nodata {
  border: 0;
}
</style>
