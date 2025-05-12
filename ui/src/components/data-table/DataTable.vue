<template>
  <div class="q-pb-lg q-pt-xs full-width full-height">
    <TableToolbar
      @change-filters="onChangeFilters"
      @change-rows-per-page="onChangeRowsPerPage"
      @change-search="onChangeSearch"
      @change-sort="onChangeSort"
      @clear-filters="onClearFilters"
      :embedded="embedded"
      :filter-list="filterList"
      :grid="grid"
      :rows-per-page="pagination.rowsPerPage"
      :search="search"
      :sort-list="sortList"
      :title="title"
    >
      <template #tableToolbar-special>
        <slot name="toolbar-special" />
      </template>

      <template #tableToolbar-filtersets>
        <slot name="toolbar-filtersets" />
      </template>
    </TableToolbar>
    <q-card class="no-border-radius-top no-border-top" bordered flat>
      <q-table
        v-model:expanded="expanded"
        v-model:pagination="pagination"
        @request="onRequest"
        :columns="columns"
        :grid="showGrid"
        :loading="loading"
        :no-data-label="noData"
        :rows="rows"
        :search="search"
        :visible-columns="visibleColumns"
        class="basic-list no-border-radius-top no-border-top"
        row-key="id"
        table-header-class="bg-grey-2"
        table-header-style="height: 35px"
        flat
        wrap-cells
      >
        <template #bottom="scope">
          <TablePager @change-page="onChangePage" :scope="scope" />
        </template>

        <template v-if="!showGrid" #header-cell="props">
          <th style="padding: 0">
            <q-item
              :class="props.col.headerClasses"
              style="height: 35px; padding-right: 10px"
              dense
            >
              <q-item-section class="text-left">
                {{ props.col.label }}
              </q-item-section>
              <q-item-section v-if="props.col.sortable" style="padding-left: 2px" side>
                <q-btn
                  @click="onChangeSort(props.col.name)"
                  size="sm"
                  style="height: 25px; width: 23px"
                  dense
                  flat
                  stack
                >
                  <q-icon
                    :color="
                      pagination.sortBy === props.col.name && !pagination.sortDesc
                        ? 'indigo-5'
                        : 'grey-5'
                    "
                    name="arrow_drop_up"
                    size="sm"
                    style="height: 9px; width: 16px"
                  />
                  <q-icon
                    v-if="props.col.sortable"
                    :color="
                      pagination.sortBy === props.col.name && pagination.sortDesc
                        ? 'indigo-5'
                        : 'grey-5'
                    "
                    name="arrow_drop_down"
                    size="sm"
                    style="height: 9px; width: 16px"
                  />
                </q-btn>
              </q-item-section>
            </q-item>
          </th>
        </template>

        <template v-if="!showGrid" #body="props">
          <q-tr :props="props">
            <q-td
              v-for="column in columns"
              :key="column.field"
              :auto-width="column.autoWidth"
              :props="props"
            >
              <slot :name="`render-cell-${column.field}`" v-bind="props">
                <template v-if="isObject(props.row[column.field])">
                  {{ props.row[column.field][column.key] }}
                </template>
                <template v-else>
                  {{ props.row[column.field] }}
                </template>
              </slot>
            </q-td>
          </q-tr>
        </template>

        <template v-if="showGrid" #item="props">
          <q-item class="full-width grid-item" dense>
            <q-item-section side top>
              <q-item-label>
                <slot name="grid-avatar" v-bind="props" />
              </q-item-label>
              <q-item-label v-if="useExpansion">
                <q-icon
                  @click="props.expand = !props.expand"
                  :name="props.expand ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer q-pa-none text-weight-bold"
                  color="indigo-3"
                  size="18px"
                  style="width: 22px; height: 16px"
                />
              </q-item-label>
            </q-item-section>

            <q-item-section>
              <q-item-label>
                <div class="row items-center">
                  <slot name="grid-main" v-bind="props" />
                </div>
              </q-item-label>
              <q-item-label>
                <slot name="grid-detail" v-bind="props" />
              </q-item-label>
            </q-item-section>

            <q-item-section style="min-width: 46px" side>
              <q-item-label class="row q-mb-auto">
                <slot name="grid-counter" v-bind="props" />
              </q-item-label>
              <q-item-label class="row full-width">
                <slot name="grid-counter-extra" v-bind="props" />
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-item
            v-if="useExpansion"
            v-show="props.expand"
            :props="props"
            class="bg-indigo-1 full-width grid-expansion-item"
            dense
          >
            <q-item-section>TESTING!</q-item-section>
          </q-item>
        </template>
      </q-table>
      <OpaqueSpinner :showing="loading" />
    </q-card>
  </div>
</template>

<script>
import { isEmpty, mapObjIndexed } from "ramda";
import { defineComponent, inject, provide, ref } from "vue";

import { OpaqueSpinner } from "@/components";
import { useStores } from "@/use";
import { isObject } from "@/utils";

import TablePager from "./TablePager.vue";
import TableToolbar from "./TableToolbar.vue";

export default defineComponent({
  name: "DataTable",
  components: {
    TableToolbar,
    OpaqueSpinner,
    TablePager,
  },
  props: {
    columns: {
      type: Object,
      required: true,
    },
    editable: {
      type: Array,
      required: false,
      default: () => [],
    },
    embedded: {
      type: Boolean,
      required: false,
      default: false,
    },
    filterList: {
      type: Object,
      required: false,
      default: () => {},
    },
    grid: {
      type: Boolean,
      required: false,
      default: false,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    noData: {
      type: String,
      required: false,
      default: "No data found",
    },
    onChangeSearch: {
      type: Function,
      required: true,
    },
    onChangePage: {
      type: Function,
      required: true,
    },
    onChangeRowsPerPage: {
      type: Function,
      required: true,
    },
    onChangeFilters: {
      type: Function,
      required: false,
      default: () => {},
    },
    onClearFilters: {
      type: Function,
      required: false,
      default: () => {},
    },
    onRequest: {
      type: Function,
      required: true,
    },
    rows: {
      type: Object,
      required: true,
    },
    schema: {
      type: Object,
      required: false,
      default: () => {},
    },
    search: {
      type: String,
      required: true,
    },
    sortList: {
      type: Array,
      required: false,
      default: () => [],
    },
    title: {
      type: String,
      required: true,
    },
    updateRequest: {
      type: Function,
      required: false,
      default: () => {},
    },
    useExpansion: {
      type: Boolean,
      required: false,
      default: false,
    },
    visibleColumns: {
      type: Array,
      required: false,
      default: () => [],
    },
    resource: {
      type: String,
      default: "",
    },
  },
  setup(props) {
    const { pagination, fetchDataPaginated } = inject("pagination");
    const { auth } = useStores();
    const expanded = ref(props.columns.map((value) => value.id));

    const schemaTypes = () => {
      if (props.schema) {
        mapObjIndexed((val) => val.type, props.schema.innerType.fields);
      }
    };

    const onChangeSort = (value) => {
      let column = null;
      let desc = false;
      if (typeof value == "object") {
        column = value.column;
        desc = value.desc;
      } else {
        column = value;
        desc = props.columns[value]["sortOrder"] === "da";
      }

      if (column === pagination.value.sortBy) {
        pagination.value.descending = !pagination.value.descending;
      } else {
        pagination.value.sortBy = column;
        pagination.value.descending = desc;
      }

      fetchDataPaginated();
    };

    const showGrid = ref(props.grid);
    provide("showGrid", showGrid);

    return {
      expanded,
      focus,
      isAdmin: auth.user.isSuperuser,
      isEmpty,
      isObject,
      onChangeSort,
      pagination,
      schemaTypes,
      showGrid,
    };
  },
});
</script>

<style lang="scss" scoped>
:deep(.basic-list .q-table__bottom) {
  min-height: 35px;
  padding: 0;
  background: #fafafa;
  border-top: none;
}
:deep(.basic-list .q-table__bottom--nodata) {
  padding-left: 12px;
}
:deep(.basic-list th) {
  padding: 0;
  border-right: 1px dotted rgb(209, 209, 209);
}
:deep(.basic-list table) {
  border-bottom: none;
}
:deep(.basic-list thead > tr > th:last-of-type) {
  border-right: none;
}
:deep(.basic-list.q-table--grid .q-table__middle) {
  min-height: 0;
  margin-bottom: 0;
}
.grid-item {
  border-top: 1px solid rgb(209, 209, 209);
  padding: 10px 15px 10px 15px;
}
.grid-item:first-of-type {
  border-top: none;
}
.grid-expansion-item {
  border-top: 1px dotted rgb(209, 209, 209);
  padding: 10px 15px 10px 15px;
}
</style>
