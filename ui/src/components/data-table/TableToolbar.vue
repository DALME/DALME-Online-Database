<template>
  <div v-if="!embedded" class="row q-mb-md">
    <div class="table-toolbar-button-group col-grow">
      <slot name="tableToolbar-special" />
      <q-btn-dropdown
        v-if="filterList && filterList.preset"
        unelevated
        no-caps
        label="Filters"
        size="12px"
        menu-anchor="bottom right"
        menu-self="top middle"
        class="bg-grey-1 text-grey-9 table-toolbar-button"
        content-class="menu-shadow"
      >
        <q-list bordered separator class="text-grey-9">
          <q-item dense class="q-pr-sm">
            <q-item-section class="text-weight-bold">
              Filter {{ title.toLowerCase() }}
            </q-item-section>
            <q-item-section avatar>
              <q-btn
                flat
                dense
                size="xs"
                color="grey-6"
                icon="close"
                @click="$emit('clearFilters')"
              />
            </q-item-section>
          </q-item>
          <template v-for="(filter, idx) in filterList.preset" :key="idx">
            <q-item
              clickable
              v-close-popup
              dense
              @click="$emit('changeFilters', filter)"
              :class="
                filter.field in activeFilters && activeFilters[filter.field] == filter.value
                  ? 'text-weight-bold bg-indigo-1 text-indigo-5'
                  : 'text-grey-8'
              "
            >
              <q-item-section>
                {{ filter.label }}
              </q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-btn-dropdown>
      <q-input
        :model-value="searchValue"
        borderless
        bg-color="grey-1"
        color="grey-9"
        hide-bottom-space
        debounce="300"
        placeholder="Search"
        autocomplete="off"
        autocorrect="off"
        autocapitalize="off"
        spellcheck="false"
        class="table-toolbar-searchbox strong-focus table-toolbar-button col-grow"
        @update:modelValue="onChangeSearchValue"
      >
        <template v-slot:append>
          <q-icon
            v-if="searchValue === ''"
            name="search"
            color="indigo-5"
            size="xs"
            class="border-radius-right"
          />
          <q-icon
            v-else
            name="close"
            class="cursor-pointer border-radius-right"
            color="indigo-5"
            size="xs"
            @click="onChangeSearchValue('')"
          />
        </template>
      </q-input>
    </div>
    <div class="table-toolbar-button-group q-ml-sm">
      <q-btn
        v-if="editable && !showGrid"
        unelevated
        :icon="isEditModeOn ? 'edit_off' : 'edit'"
        size="10px"
        :color="isEditModeOn ? 'red-2' : 'white'"
        :text-color="isEditModeOn ? 'red-4' : 'grey-9'"
        class="btn-icon table-toolbar-button"
        @click="isEditModeOn = !isEditModeOn"
      >
        <ToolTip v-if="editable">
          Click on this button to enable editing data in place for supported columns (marked with
          this same icon).
        </ToolTip>
      </q-btn>
      <q-btn-dropdown
        v-if="!showGrid"
        unelevated
        icon="o_view_week"
        size="10px"
        color="white"
        text-color="grey-8"
        class="table-toolbar-button"
        content-class="menu-shadow"
      >
        <q-list padding bordered dense>
          <q-item
            v-for="(value, idx) in columns"
            :key="idx"
            dense
            clickable
            v-ripple
            v-close-popup
            class="text-grey-8"
            @click="onChangeColumnVisibility(value.name)"
          >
            <q-item-section side class="q-pr-sm">
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
        unelevated
        no-caps
        size="10px"
        color="white"
        text-color="grey-8"
        class="table-toolbar-button"
        content-class="menu-shadow"
      >
        <template v-slot:label>
          <span style="font-size: 12px">Show {{ currentRpP }} rows</span>
        </template>
        <q-list padding bordered dense>
          <q-item
            v-for="(value, idx) in rowsPerPageOptions"
            :key="idx"
            dense
            clickable
            v-ripple
            v-close-popup
            :class="
              value.value === rowsPerPageValue
                ? 'text-weight-bold bg-indigo-1 text-indigo-5'
                : 'text-grey-8'
            "
            @click="onChangeRowsPerPageValue(value.value)"
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
        unelevated
        :icon="showGrid ? 'o_table_chart' : 'o_table_rows'"
        size="10px"
        color="white"
        text-color="grey-9"
        class="btn-icon table-toolbar-button"
        @click="showGrid = !showGrid"
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
          v-bind="filterSet"
          @item-chosen="
            (v) =>
              $emit('changeFilters', {
                field: filterSet.field,
                value: v,
                selection: filterSet.selection,
                isolation: filterSet.isolation,
              })
          "
          @clear-filters="$emit('clearFilters')"
        />
      </template>
    </template>
    <q-btn-dropdown
      v-if="sortList"
      flat
      dense
      label="Sort"
      menu-anchor="bottom right"
      menu-self="top right"
      class="text-capitalize"
      content-class="menu-shadow"
    >
      <q-list bordered separator class="text-grey-9">
        <q-item dense>
          <q-item-section class="text-weight-bold">Sort by</q-item-section>
        </q-item>
        <template v-for="(item, idx) in sortList" :key="idx">
          <q-item
            clickable
            v-close-popup
            dense
            :class="
              item.value.column === pagination.sortBy && item.value.desc === pagination.descending
                ? 'text-no-wrap text-weight-bold bg-indigo-1 text-indigo-5'
                : 'text-no-wrap text-grey-8'
            "
            @click="$emit('changeSort', item.value)"
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
import { useRoute } from "vue-router";
import { filter as rFilter } from "ramda";
import { computed, defineComponent, inject, ref, watch } from "vue";
import { ToolTip, FilterChooser } from "@/components";

export default defineComponent({
  name: "TableToolbar",
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
  components: {
    FilterChooser,
    ToolTip,
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
      console.log("watcher: isEditModeOn", newValue);
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

<style lang="scss">
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
button.table-toolbar-button.btn-icon {
  padding-right: 10px;
}
.table-toolbar-button {
  border-top: 1px solid rgb(209, 209, 209);
  border-bottom: 1px solid rgb(209, 209, 209);
  border-right: 1px solid rgb(209, 209, 209);
  border-radius: 0;
}
.table-toolbar-searchbox .q-field__control,
.table-toolbar-searchbox .q-field__marginal {
  font-size: 13px;
  height: 28px;
  padding: 0px 5px 0px 10px;
  border-radius: 4px;
}
.table-toolbar-searchbox .q-field__native {
  font-weight: 500;
}
.table-toolbar-searchbox .q-field__inner {
  align-self: center;
}
</style>
