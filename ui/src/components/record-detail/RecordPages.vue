<template>
  <q-table
    flat
    dense
    :rows="pages"
    :columns="columns"
    :no-data-label="noData"
    :filter="filter"
    :pagination="pagination"
    :rows-per-page-options="[0]"
    row-key="id"
    class="sticky-header"
    table-colspan="5"
    wrap-cells
  >
    <template v-slot:body-cell-hasImage="props">
      <q-td :props="props"><BooleanValue :value="props.value" /></q-td>
    </template>

    <template v-slot:body-cell-hasTranscription="props">
      <q-td :props="props"><BooleanValue :value="props.value" /></q-td>
    </template>
  </q-table>
</template>

<script>
import { defineComponent, inject } from "vue";
import { BooleanValue } from "@/components";

export default defineComponent({
  name: "RecordPages",
  props: {
    pages: {
      type: Array,
      required: true,
    },
  },
  components: {
    BooleanValue,
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
