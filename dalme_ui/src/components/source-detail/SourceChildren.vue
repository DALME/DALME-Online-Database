<template>
  <q-item
    :dense="overview"
    class="q-pb-none q-px-sm text-indigo-5"
    :class="overview ? 'bg-indigo-1' : ''"
  >
    <q-item-section side class="q-pr-sm">
      <q-icon name="account_tree" color="indigo-5" size="xs" />
    </q-item-section>
    <q-item-section>
      <q-item-label :class="overview ? 'text-subtitle2' : 'text-h6'">
        Children
        <q-badge rounded color="purple-4" align="middle">
          {{ children.length }}
        </q-badge>
      </q-item-label>
    </q-item-section>
    <q-space />
    <q-input
      :dense="overview"
      :standout="overview ? 'bg-indigo-3 no-shadow' : false"
      :bg-color="overview ? 'indigo-2' : 'inherit'"
      :color="overview ? 'indigo-6' : 'inherit'"
      placeholder="Filter"
      hide-bottom-space
      v-model="filter"
      debounce="300"
      autocomplete="off"
      autocorrect="off"
      autocapitalize="off"
      spellcheck="false"
      :class="overview ? 'card-title-search' : ''"
    >
      <template v-slot:append>
        <q-icon
          v-if="filter === ''"
          name="search"
          color="indigo-5"
          :size="overview ? '14px' : 'sm'"
        />
        <q-icon
          v-else
          name="highlight_off"
          class="cursor-pointer"
          color="indigo-5"
          :size="overview ? '14px' : 'sm'"
          @click="filter = ''"
        />
      </template>
    </q-input>
  </q-item>

  <q-separator class="bg-indigo-5" />

  <q-table
    :flat="!overview"
    :dense="overview"
    :rows="children"
    :columns="columns"
    :visible-columns="visibleColumns"
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
        <router-link
          class="text-link"
          :to="{
            name: 'Source',
            params: { id: props.row.id },
          }"
        >
          {{ props.value }}
        </router-link>
      </q-td>
    </template>

    <template v-slot:body-cell-type="props">
      <q-td :props="props" class="text-no-wrap">
        {{ props.value }}
        <q-chip
          v-if="props.row.hasInventory"
          dense
          size="10px"
          outline
          color="green-9"
          class="text-bold"
        >
          LIST
        </q-chip>
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, ref } from "vue";

const columnMap = {
  name: "Name",
  shortName: "Short Name",
  type: "Type",
  hasInventory: "Inventory",
};

export default defineComponent({
  name: "SourceChildren",
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
    const visibleColumns = ref(
      props.overview ? ["name", "type"] : ["name", "shortName", "type"],
    );
    const filter = ref("");

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
