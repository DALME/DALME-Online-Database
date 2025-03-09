<template>
  <template v-if="overview">
    <q-table
      flat
      :dense="overview"
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
  <template v-else>
    <RecordEditor />
  </template>
</template>

<script>
import { defineComponent, inject, provide, ref } from "vue";
import { getColumns } from "@/utils";
import { BooleanValue, RecordEditor } from "@/components";
import { columnMap } from "./pageColumns";

export default defineComponent({
  name: "RecordPages",
  props: {
    pages: {
      type: Array,
      required: true,
    },
    overview: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  components: {
    BooleanValue,
    RecordEditor,
  },
  setup(props) {
    const columns = ref(getColumns(columnMap));
    const filter = props.overview ? inject("cardFilter") : ref("");
    const noData = "No folios found.";
    const pagination = { rowsPerPage: 0 }; // All rows.

    provide("pages", props.pages);
    provide("columns", columns);

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
