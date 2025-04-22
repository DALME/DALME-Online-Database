<template>
  <div v-if="!embedded" class="row q-mb-md">
    <div class="table-toolbar-button-group col-grow">
      <slot name="tableToolbar-special" />
      <q-btn-dropdown
        v-if="filterList && filterList.preset"
        class="bg-grey-1 text-grey-9 table-toolbar-button"
        content-class="menu-shadow"
        label="Filters"
        menu-anchor="bottom right"
        menu-self="top middle"
        size="12px"
        no-caps
        unelevated
      >
        <q-list class="text-grey-9" bordered separator>
          <q-item class="q-pr-sm" dense>
            <q-item-section class="text-weight-bold">
              Filter {{ title.toLowerCase() }}
            </q-item-section>
            <q-item-section avatar>
              <q-btn
                @click="$emit('clearFilters')"
                color="grey-6"
                icon="close"
                size="xs"
                dense
                flat
              />
            </q-item-section>
          </q-item>
          <template v-for="(filter, idx) in filterList.preset" :key="idx">
            <q-item
              v-close-popup
              @click="$emit('changeFilters', filter)"
              :class="
                filter.field in activeFilters && activeFilters[filter.field] == filter.value
                  ? 'text-weight-bold bg-indigo-1 text-indigo-5'
                  : 'text-grey-8'
              "
              clickable
              dense
            >
              <q-item-section>
                {{ filter.label }}
              </q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-btn-dropdown>
      <q-input
        @update:model-value="onChangeSearchValue"
        :model-value="searchValue"
        autocapitalize="off"
        autocomplete="off"
        autocorrect="off"
        bg-color="grey-1"
        class="table-toolbar-searchbox strong-focus table-toolbar-button col-grow"
        color="grey-9"
        debounce="300"
        placeholder="Search"
        spellcheck="false"
        borderless
        hide-bottom-space
      >
        <template #append>
          <q-icon
            v-if="searchValue === ''"
            class="border-radius-right"
            color="indigo-5"
            name="search"
            size="xs"
          />
          <q-icon
            v-else
            @click="onChangeSearchValue('')"
            class="cursor-pointer border-radius-right"
            color="indigo-5"
            name="close"
            size="xs"
          />
        </template>
      </q-input>
    </div>
    <div class="table-toolbar-button-group q-ml-sm">
      <q-btn
        v-if="editable && !showGrid"
        @click="isEditModeOn = !isEditModeOn"
        :color="isEditModeOn ? 'red-2' : 'white'"
        :icon="isEditModeOn ? 'edit_off' : 'edit'"
        :text-color="isEditModeOn ? 'red-4' : 'grey-9'"
        class="btn-icon table-toolbar-button"
        size="10px"
        unelevated
      >
        <ToolTip v-if="editable">
          Click on this button to enable editing data in place for supported columns (marked with
          this same icon).
        </ToolTip>
      </q-btn>
      <q-btn-dropdown
        v-if="!showGrid"
        class="table-toolbar-button"
        color="white"
        content-class="menu-shadow"
        icon="o_view_week"
        size="10px"
        text-color="grey-8"
        unelevated
      >
        <q-list bordered dense padding>
          <q-item
            v-for="(value, idx) in columns"
            :key="idx"
            v-close-popup
            v-ripple
            @click="onChangeColumnVisibility(value.name)"
            class="text-grey-8"
            clickable
            dense
          >
            <q-item-section class="q-pr-sm" side>
              <q-icon
                :name="
                  visibleColumns.includes(value.name) ? 'check_box' : 'check_box_outline_blank'
                "
                color="indigo-5"
                size="xs"
              />
            </q-item-section>
            <q-item-section class="q-pr-sm">
              <q-item-label>{{ value.label }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <ToolTip>Select which columns should be displayed.</ToolTip>
      </q-btn-dropdown>
      <q-btn-dropdown
        class="table-toolbar-button"
        color="white"
        content-class="menu-shadow"
        size="10px"
        text-color="grey-8"
        no-caps
        unelevated
      >
        <template #label>
          <span style="font-size: 12px">Show {{ currentRpP }} rows</span>
        </template>
        <q-list bordered dense padding>
          <q-item
            v-for="(value, idx) in rowsPerPageOptions"
            :key="idx"
            v-close-popup
            v-ripple
            @click="onChangeRowsPerPageValue(value.value)"
            :class="
              value.value === rowsPerPageValue
                ? 'text-weight-bold bg-indigo-1 text-indigo-5'
                : 'text-grey-8'
            "
            clickable
            dense
          >
            <q-item-section>
              <q-item-label>{{ value.label }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <ToolTip>Select how many records to display per page.</ToolTip>
      </q-btn-dropdown>
      <q-btn
        v-if="grid"
        @click="showGrid = !showGrid"
        :icon="showGrid ? 'o_table_chart' : 'o_table_rows'"
        class="btn-icon table-toolbar-button"
        color="white"
        size="10px"
        text-color="grey-9"
        unelevated
      >
        <ToolTip>Switch between table and grid view.</ToolTip>
      </q-btn>
    </div>
  </div>
  <q-toolbar
    class="full-width outlined-item border-radius-top no-border-radius-bottom bg-grey-1 text-grey-8"
  >
    <div class="text-detail text-weight-medium">
      {{ paginationStatus }}
    </div>
    <q-space />
    <slot name="tableToolbar-filtersets" />
    <template v-if="filterList && filterList.filters">
      <template v-for="(filterSet, idx) in filterList.filters" :key="idx">
        <FilterChooser
          @clear-filters="$emit('clearFilters')"
          @item-chosen="
            (v) =>
              $emit('changeFilters', {
                field: filterSet.field,
                value: v,
                selection: filterSet.selection,
                isolation: filterSet.isolation,
              })
          "
          v-bind="filterSet"
        />
      </template>
    </template>
    <q-btn-dropdown
      v-if="sortList"
      class="text-capitalize"
      content-class="menu-shadow"
      label="Sort"
      menu-anchor="bottom right"
      menu-self="top right"
      dense
      flat
    >
      <q-list class="text-grey-9" bordered separator>
        <q-item dense>
          <q-item-section class="text-weight-bold">Sort by</q-item-section>
        </q-item>
        <template v-for="(item, idx) in sortList" :key="idx">
          <q-item
            v-close-popup
            @click="$emit('changeSort', item.value)"
            :class="
              item.value.column === pagination.sortBy && item.value.desc === pagination.descending
                ? 'text-no-wrap text-weight-bold bg-indigo-1 text-indigo-5'
                : 'text-no-wrap text-grey-8'
            "
            clickable
            dense
          >
            <q-item-section>
              {{ item.label }}
            </q-item-section>
          </q-item>
        </template>
      </q-list>
    </q-btn-dropdown>
  </q-toolbar>
</template>

<script>
import { filter as rFilter } from "ramda";
import { computed, defineComponent, inject, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { FilterChooser, ToolTip } from "@/components";

export default defineComponent({
  name: "TableToolbar",
  components: {
    FilterChooser,
    ToolTip,
  },
  props: {
    editable: {
      type: Boolean,
      required: false,
      default: false,
    },
    embedded: {
      type: Boolean,
      required: true,
    },
    filterList: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    grid: {
      type: Boolean,
      required: true,
    },
    rowsPerPage: {
      type: Number,
      required: true,
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
    resource: {
      type: String,
      default: "",
    },
  },
  emits: [
    "changeRowsPerPage",
    "changeSearch",
    "changeEditMode",
    "changeSort",
    "changeFilters",
    "clearFilters",
  ],
  setup(props, context) {
    const $route = useRoute();
    const resource = computed(() => props.resource || $route.name.toLowerCase());
    const { pagination } = inject("pagination");
    const showGrid = inject("showGrid");
    const activeFilters = props.filterList ? inject("activeFilters") : ref({});

    const rowsPerPageOptions = [
      { label: 10, value: 10 },
      { label: 20, value: 20 },
      { label: 30, value: 30 },
      { label: 40, value: 40 },
      { label: 50, value: 50 },
      { label: "All", value: 0 },
    ];
    const columns = inject("columns");
    const visibleColumns = inject("visibleColumns");
    const rowsPerPageValue = ref(props.rowsPerPage);
    const searchValue = ref(props.search);
    const isEditModeOn = ref(false);

    const currentRpP = computed(() => {
      return rFilter((item) => item.value == rowsPerPageValue.value, rowsPerPageOptions)[0][
        "label"
      ];
    });

    const onChangeColumnVisibility = (value) => {
      if (visibleColumns.value.includes(value)) {
        visibleColumns.value.splice(visibleColumns.value.indexOf(value), 1);
      } else {
        visibleColumns.value.push(value);
      }
    };

    const onChangeRowsPerPageValue = (value) => {
      rowsPerPageValue.value = value;
      context.emit("changeRowsPerPage", value);
    };

    const onChangeSearchValue = (value) => {
      searchValue.value = value;
      context.emit("changeSearch", value);
    };

    const paginationStatus = computed(() => {
      let rangeStart = (pagination.value.page - 1) * pagination.value.rowsPerPage + 1;
      let rangeEnd = rangeStart + pagination.value.rowsPerPage - 1;
      if (rangeEnd > pagination.value.rowsNumber) rangeEnd = pagination.value.rowsNumber;

      return `Showing ${rangeStart.toLocaleString("en-US")}-${rangeEnd.toLocaleString(
        "en-US",
      )} out of a total of ${pagination.value.rowsNumber.toLocaleString(
        "en-US",
      )} ${resource.value}.`;
    });

    watch(isEditModeOn, (newValue) => {
      context.emit("changeFilters", newValue);
    });

    return {
      activeFilters,
      columns,
      currentRpP,
      searchValue,
      isEditModeOn,
      onChangeColumnVisibility,
      onChangeSearchValue,
      onChangeRowsPerPageValue,
      pagination,
      paginationStatus,
      rowsPerPageOptions,
      rowsPerPageValue,
      showGrid,
      visibleColumns,
    };
  },
});
</script>

<style lang="scss" scoped>
.table-toolbar-button-group {
  display: inline-flex;
}
.table-toolbar-button-group .table-toolbar-button:first-child {
  border-left: 1px solid rgb(209, 209, 209);
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}
.table-toolbar-button-group .table-toolbar-button:last-child {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
}
button.table-toolbar-button {
  min-height: 2em;
  padding: 4px 5px 4px 10px;
}
:deep(button.table-toolbar-button.btn-icon) {
  padding-right: 10px;
}
.table-toolbar-button {
  border-top: 1px solid rgb(209, 209, 209);
  border-bottom: 1px solid rgb(209, 209, 209);
  border-right: 1px solid rgb(209, 209, 209);
  border-radius: 0;
}
:deep(.table-toolbar-searchbox .q-field__control),
:deep(.table-toolbar-searchbox .q-field__marginal) {
  font-size: 13px;
  height: 28px;
  padding: 0px 5px 0px 10px;
  border-radius: 4px;
}
:deep(.table-toolbar-searchbox .q-field__native) {
  font-weight: 500;
}
:deep(.table-toolbar-searchbox .q-field__inner) {
  align-self: center;
}
</style>
