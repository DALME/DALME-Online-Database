<template>
  <q-tabs
    v-model="tab"
    dense
    class="text-grey"
    active-color="primary"
    indicator-color="primary"
    align="left"
    narrow-indicator
  >
    <q-tab name="list" label="List" />
    <q-tab name="editor" label="View/Edit" />
  </q-tabs>
  <q-separator />
  <q-tab-panels v-model="tab" animated>
    <q-tab-panel name="list">
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
            Folios ({{ pages.length }})
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
    </q-tab-panel>
    <q-tab-panel name="editor">
      <SourceEditor />
    </q-tab-panel>
  </q-tab-panels>
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, inject, provide, ref } from "vue";
import SourceEditor from "./SourceEditor.vue";

const columnMap = {
  damId: "DAM ID",
  name: "Name",
  order: "Order",
  hasImage: "Image",
  hasTranscription: "Transcribed",
};

export default defineComponent({
  name: "SourcePages",
  components: {
    SourceEditor,
  },
  setup() {
    const columns = ref([]);
    const filter = ref("");
    const source = inject("source");
    const pages = source.value.pages;

    const currentFolio = ref(0);
    const updatecurrentFolio = (value) => {
      currentFolio.value = value;
    };

    const noData = "No pages found.";
    const pagination = { rowsPerPage: 0 }; // All rows.
    const tab = ref("list");

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

    provide("pages", pages);
    provide("currentFolio", { currentFolio, updatecurrentFolio });

    return {
      columns,
      filter,
      noData,
      pages,
      pagination,
      rows: pages,
      tab,
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
