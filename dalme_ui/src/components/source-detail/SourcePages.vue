<template>
  <q-table
    :rows="rows"
    :columns="columns"
    :no-data-label="noData"
    :filter="filter"
    :pagination="pagination"
    :rows-per-page-options="[0]"
    row-key="id"
    class="sticky-header"
  >
    <template v-slot:top>
      <q-item-section avatar>
        <q-avatar>
          <q-icon name="menu_book" />
        </q-avatar>
      </q-item-section>
      <q-item-label class="text-weight-medium">
        Pages ({{ pages.length }})
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

    <template v-slot:body-cell-hasImage="props">
      <q-td :props="props">
        <q-icon :name="props.value ? 'done' : 'close'" size="xs" />
      </q-td>
    </template>

    <template v-slot:body-cell-hasTranscription="props">
      <q-td :props="props">
        <q-icon :name="props.value ? 'done' : 'close'" size="xs" />
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, ref } from "vue";

const columnMap = {
  damId: "DAM ID",
  name: "Name",
  order: "Order",
  hasImage: "Image",
  hasTranscription: "Transcribed",
};

export default defineComponent({
  name: "SourcePages",
  props: {
    pages: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const columns = ref([]);
    const filter = ref("");

    const noData = "No pages found.";
    const pagination = { rowsPerPage: 0 }; // All rows.

    const getColumns = () => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys(columnMap));
    };
    columns.value = getColumns();

    return {
      columns,
      filter,
      noData,
      pagination,
      rows: props.pages,
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
