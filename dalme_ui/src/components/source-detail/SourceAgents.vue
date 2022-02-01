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
          <q-icon name="people" />
        </q-avatar>
      </q-item-section>
      <q-item-label class="text-weight-medium">
        Agents ({{ agents.length }})
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
        <span v-html="props.value"></span>
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, ref } from "vue";

const columnMap = {
  name: "Standard Name",
  type: "Type",
  legalPersona: "Legal Persona",
};

export default defineComponent({
  name: "SourceAgents",
  props: {
    agents: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const columns = ref([]);
    const visibleColumns = ref([]);
    const filter = ref("");

    const noData = "No agents found.";
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
      visibleColumns,
      filter,
      noData,
      pagination,
      rows: props.agents,
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
