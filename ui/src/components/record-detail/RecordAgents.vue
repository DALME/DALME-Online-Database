<template>
  <q-table
    flat
    :dense="overview"
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
import { keys, map } from "ramda";
import { defineComponent, inject, ref } from "vue";

const columnMap = {
  name: "Standard Name",
  type: "Type",
  legalPersona: "Legal Persona",
};

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
  setup(props) {
    const columns = ref([]);
    const visibleColumns = ref([]);
    const filter = inject("cardFilter");

    const noData = "No agents found.";
    const pagination = { rowsPerPage: props.overview ? 5 : 0 }; // 0 = all rows

    const getColumns = () => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
        headerClasses: "text-no-wrap",
      });
      return map(toColumn, keys(columnMap));
    };
    columns.value = getColumns();

    return {
      columns,
      visibleColumns,
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
