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
        Set Members ({{ memberCount }}, {{ publicMemberCount }} public)
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
  </q-table>
</template>

<script>
import { map } from "ramda";
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "SetMembers",
  props: {
    members: {
      type: Array,
      required: true,
    },
    memberCount: {
      type: Number,
      required: true,
    },
    publicMemberCount: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const columns = ref([]);
    const filter = ref("");

    const noData = "No members found.";
    const pagination = { rowsPerPage: 0 }; // All rows.

    const getColumns = () => {
      const columnMap = {
        objId: "ID",
        name: "Name",
      };
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, ["objId", "name"]);
    };
    columns.value = getColumns();

    return {
      columns,
      filter,
      noData,
      pagination,
      rows: props.members,
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
