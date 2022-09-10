<template>
  <q-item
    :dense="overview"
    class="q-pb-none q-px-sm text-indigo-5"
    :class="overview ? 'bg-indigo-1' : ''"
  >
    <q-item-section side class="q-pr-sm">
      <q-icon name="place" color="indigo-5" size="xs" />
    </q-item-section>
    <q-item-section>
      <q-item-label :class="overview ? 'text-subtitle2' : 'text-h6'">
        Places
        <q-badge rounded color="purple-4" align="middle">
          {{ places.length }}
        </q-badge>
      </q-item-label>
    </q-item-section>
    <q-space />
    <q-input
      :dense="overview"
      :standout="overview ? 'bg-indigo-3 no-shadow' : false"
      :bg-color="overview ? 'indigo-1' : 'inherit'"
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
import { defineComponent, ref } from "vue";

const columnMap = {
  placename: "Placename",
  locale: "Locale",
};

export default defineComponent({
  name: "SourcePlaces",
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
    const filter = ref("");

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
