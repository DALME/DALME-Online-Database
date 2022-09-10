<template>
  <template v-if="overview">
    <q-item
      :dense="overview"
      class="q-pb-none q-px-sm text-indigo-5"
      :class="overview ? 'bg-indigo-1' : ''"
    >
      <q-item-section side class="q-pr-sm">
        <q-icon name="auto_stories" color="indigo-5" size="xs" />
      </q-item-section>
      <q-item-section>
        <q-item-label :class="overview ? 'text-subtitle2' : 'text-h6'">
          Folios
          <q-badge rounded color="purple-4" align="middle">
            {{ pages.length }}
          </q-badge>
        </q-item-label>
      </q-item-section>
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
      :rows="pages"
      :columns="columns"
      :no-data-label="noData"
      :filter="filter"
      :pagination="pagination"
      :rows-per-page-options="[0]"
      row-key="id"
      class="sticky-header"
      table-colspan="5"
      wrap-cells
    >
      <template v-slot:body-cell-hasImage="props">
        <q-td :props="props">
          <q-icon
            :name="props.value ? 'check_box' : 'disabled_by_default'"
            :color="props.value ? 'green-9' : 'red-10'"
            size="xs"
          />
        </q-td>
      </template>

      <template v-slot:body-cell-hasTranscription="props">
        <q-td :props="props">
          <q-icon
            :name="!props.value ? 'check_box' : 'disabled_by_default'"
            :color="!props.value ? 'green-9' : 'red-10'"
            size="xs"
          />
        </q-td>
      </template>
    </q-table>
  </template>
  <template v-else>
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
          :rows="pages"
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
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, provide, ref } from "vue";
import SourceEditor from "./SourceEditor.vue";

const columnMap = {
  damId: {
    label: "DAM ID",
  },
  name: {
    label: "Name",
  },
  order: {
    label: "Order",
  },
  hasImage: {
    label: "Image",
    align: "center",
  },
  hasTranscription: {
    label: "Transcribed",
    align: "center",
  },
};

export default defineComponent({
  name: "SourcePages",
  props: {
    pages: {
      type: Object,
      required: true,
    },
    overview: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  components: {
    SourceEditor,
  },
  setup(props) {
    const columns = ref([]);
    const filter = ref("");

    const currentFolio = ref(0);
    const updatecurrentFolio = (value) => {
      currentFolio.value = value;
    };

    const noData = "No pages found.";
    const pagination = { rowsPerPage: 0 }; // All rows.
    const tab = ref("list");

    const getColumns = () => {
      const toColumn = (key) => ({
        align: columnMap[key]["align"] || "left",
        field: key,
        label: columnMap[key]["label"],
        name: key,
        sortable: columnMap[key]["sort"] || true,
        classes: columnMap[key]["class"] || null,
        headerClasses: columnMap[key]["headerClass"] || "text-no-wrap",
      });
      return map(toColumn, keys(columnMap));
    };
    columns.value = getColumns();

    provide("pages", props.pages);
    provide("currentFolio", { currentFolio, updatecurrentFolio });

    return {
      columns,
      filter,
      noData,
      pagination,
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
