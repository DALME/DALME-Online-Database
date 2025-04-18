<template>
  <q-table
    :columns="columns"
    :dense="overview"
    :filter="filter"
    :no-data-label="noData"
    :pagination="pagination"
    :rows="children"
    :rows-per-page-options="[0]"
    :visible-columns="visibleColumns"
    class="sticky-header"
    row-key="id"
    table-colspan="3"
    flat
    wrap-cells
  >
    <template #body-cell-name="props">
      <q-td :props="props">
        <router-link
          :to="{
            name: 'Record',
            params: { id: props.row.id },
          }"
          class="text-link"
        >
          {{ props.value }}
        </router-link>
      </q-td>
    </template>

    <template #body-cell-type="props">
      <q-td :props="props" class="text-no-wrap">
        {{ props.value }}
        <q-chip
          v-if="props.row.hasInventory"
          class="text-bold"
          color="green-9"
          size="10px"
          dense
          outline
        >
          LIST
        </q-chip>
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, inject, ref } from "vue";

const columnMap = {
  name: "Name",
  shortName: "Short Name",
  type: "Type",
  hasInventory: "Inventory",
};

export default defineComponent({
  name: "RecordChildren",
  props: {
    children: {
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
    const visibleColumns = ref(props.overview ? ["name", "type"] : ["name", "shortName", "type"]);
    const filter = inject("cardFilter");

    const noData = "No children found.";
    const pagination = { rowsPerPage: props.overview ? 10 : 0 }; // 0 = all rows

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
      filter,
      noData,
      pagination,
      visibleColumns,
    };
  },
});
</script>
