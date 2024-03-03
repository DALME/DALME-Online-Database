<template>
  <q-table
    flat
    :dense="overview"
    :rows="places"
    :columns="columns"
    :no-data-label="noData"
    :filter="filter"
    :pagination="pagination"
    :rows-per-page-options="[0]"
    row-key="id"
    class="sticky-header"
    table-colspan="2"
    wrap-cells
  />
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, inject, ref } from "vue";

const columnMap = {
  placename: "Placename",
  locale: "Locale",
};

export default defineComponent({
  name: "RecordPlaces",
  props: {
    places: {
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
    const filter = inject("cardFilter");

    const noData = "No places found.";
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
      filter,
      noData,
      pagination,
    };
  },
});
</script>
