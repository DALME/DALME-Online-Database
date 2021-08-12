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
    class="sticky-header"
  >
    <template v-slot:top>
      <q-item-section avatar>
        <q-avatar>
          <q-icon name="menu_book" />
        </q-avatar>
      </q-item-section>
      <q-item-label class="text-weight-medium">
        Children ({{ children.length }})
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

    <template v-slot:body-cell-name="props">
      <q-td :props="props">
        <router-link
          :to="{
            name: 'Source',
            params: { objId: props.row.objId },
          }"
        >
          {{ props.value }}
        </router-link>
      </q-td>
    </template>

    <template v-slot:body-cell-hasInventory="props">
      <q-td :props="props">
        <q-icon :name="props.value ? 'done' : 'close'" size="xs" />
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { filter as rFilter, keys, map } from "ramda";
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "SourceChildren",
  props: {
    children: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const columns = ref([]);
    const visibleColumns = ref([]);
    const filter = ref("");

    const noData = "No children found.";
    const pagination = { rowsPerPage: 0 }; // All rows.

    const getColumns = (keys) => {
      const columnMap = {
        name: "Name",
        shortName: "Short Name",
        type: "Type",
        hasInventory: "Inventory",
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
    columns.value = getColumns(keys(props.children[0]));
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
      rows: props.children,
    };
  },
});
</script>
