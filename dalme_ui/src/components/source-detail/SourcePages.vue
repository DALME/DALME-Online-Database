<template>
  <template v-if="overview">
    <q-table
      flat
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
        <q-td :props="props"><BooleanIcon :value="props.value" /></q-td>
      </template>

      <template v-slot:body-cell-hasTranscription="props">
        <q-td :props="props"><BooleanIcon :value="props.value" /></q-td>
      </template>
    </q-table>
  </template>
  <template v-else>
    <q-layout view="lHr LpR lFr" container style="height: 500px">
      <q-drawer
        v-model="leftDrawer"
        side="left"
        :mini="leftMini"
        mini-to-overlay
        class="detail-drawer-left"
        width="300"
        mini-width="40"
      >
        <div class="row q-pt-sm q-pl-sm">
          <q-icon
            name="o_auto_stories"
            size="20px"
            :color="leftMini ? 'grey-7' : 'indigo-6'"
            class="cursor-pointer"
            @click="leftMini = !leftMini"
          />
          <span class="text-h7 q-ml-sm q-mini-drawer-hide">Folios</span>
        </div>
        <q-table
          :rows="pages"
          :columns="columns"
          :no-data-label="noData"
          :filter="filter"
          :pagination="pagination"
          :rows-per-page-options="[0]"
          row-key="id"
          class="sticky-header q-mini-drawer-hide"
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
            <q-td :props="props"><BooleanIcon :value="props.value" /></q-td>
          </template>

          <template v-slot:body-cell-hasTranscription="props">
            <q-td :props="props"><BooleanIcon :value="props.value" /></q-td>
          </template>
        </q-table>
      </q-drawer>

      <q-drawer
        v-model="rightDrawer"
        side="right"
        :mini="rightMini"
        mini-to-overlay
        class="detail-drawer-right"
        width="300"
        mini-width="40"
      >
        <!-- drawer content -->
      </q-drawer>

      <q-page-container>
        <q-page class="q-px-sm">
          <SourceEditor />
        </q-page>
      </q-page-container>
    </q-layout>
  </template>
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, inject, provide, ref } from "vue";
import { BooleanIcon } from "@/components/utils";
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
    BooleanIcon,
    SourceEditor,
  },
  setup(props) {
    const columns = ref([]);
    const filter = props.overview ? inject("cardFilter") : ref("");
    const leftDrawer = ref(true);
    const rightDrawer = ref(true);
    const leftMini = ref(true);
    const rightMini = ref(true);

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
      leftDrawer,
      rightDrawer,
      leftMini,
      rightMini,
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
