<template>
  <q-table
    flat
    dense
    :rows="agents"
    :columns="columns"
    :no-data-label="noData"
    :filter="filter"
    :pagination="pagination"
    :rows-per-page-options="[0]"
    row-key="id"
    class="sticky-header"
    table-colspan="3"
    wrap-cells
  >
    <template v-slot:body-cell-name="props">
      <q-td :props="props">
        <span v-html="props.value" />
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { defineComponent, inject, ref } from "vue";
import { getColumns } from "@/utils";
import { columnMap } from "./agentColumns";

export default defineComponent({
  name: "RecordAgents",
  props: {
    agents: {
      type: Object,
      required: true,
    },
    overview: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  setup() {
    const columns = ref(getColumns(columnMap));
    const filter = inject("cardFilter");
    const noData = "No agents found.";
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

<style lang="scss">
.q-table__top {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding: 0;
}
.q-table__bottom--nodata {
  border: 0;
}
</style>
