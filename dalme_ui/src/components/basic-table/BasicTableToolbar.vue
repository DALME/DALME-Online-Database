<template>
  <q-item dense class="q-pa-xs bg-indigo-1 text-indigo-5">
    <q-item-section side class="q-pl-xs q-pr-sm">
      <q-icon name="list" color="indigo-5" size="sm" />
    </q-item-section>
    <q-item-section>
      <q-item-label class="text-subtitle text-weight-bold">
        List of {{ title }}
      </q-item-label>
    </q-item-section>
    <q-item-section side class="q-mr-xs">
      <q-btn-group unelevated style="height: 28px">
        <q-btn
          v-if="editable"
          unelevated
          :icon="isEditModeOn ? 'edit_off' : 'edit'"
          size="12px"
          :color="isEditModeOn ? 'red-2' : 'indigo-2'"
          :text-color="isEditModeOn ? 'red-4' : 'indigo-5'"
          class="list-title-button btn-icon"
          @click="isEditModeOn = !isEditModeOn"
        >
          <Tooltip v-if="editable">
            Click on this button to enable editing data in place for supported
            columns (marked with this same icon).
          </Tooltip>
        </q-btn>
        <q-separator v-if="editable" vertical class="bg-indigo-1" />
        <q-btn-dropdown
          unelevated
          icon="view_week"
          size="12px"
          color="indigo-2"
          text-color="indigo-5"
          class="list-title-button"
        >
          <q-list padding dense>
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
                    visibleColumns.includes(value.name)
                      ? 'check_box'
                      : 'check_box_outline_blank'
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
          <Tooltip>Select which columns should be displayed.</Tooltip>
        </q-btn-dropdown>
        <q-separator vertical class="bg-indigo-1" />
        <q-btn-dropdown
          unelevated
          no-caps
          size="12px"
          color="indigo-2"
          text-color="indigo-5"
          class="list-title-button"
          :label="`Show ${rowsPerPageValue} rows`"
        >
          <q-list padding dense>
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
          <Tooltip>Select how many rows to display per page.</Tooltip>
        </q-btn-dropdown>
      </q-btn-group>
    </q-item-section>
    <q-input
      :model-value="filterValue"
      standout="bg-indigo-3 no-shadow"
      bg-color="indigo-2"
      color="indigo-6"
      dense
      hide-bottom-space
      debounce="300"
      placeholder="Filter"
      autocomplete="off"
      autocorrect="off"
      autocapitalize="off"
      spellcheck="false"
      class="list-title-search"
      @update:modelValue="onChangeFilterValue"
    >
      <template v-slot:append>
        <q-icon
          v-if="filterValue === ''"
          name="search"
          color="indigo-5"
          size="xs"
        />
        <q-icon
          v-else
          name="highlight_off"
          class="cursor-pointer"
          color="indigo-5"
          size="xs"
          @click="onChangeFilterValue('')"
        />
      </template>
    </q-input>
  </q-item>
</template>

<script>
import { defineAsyncComponent, defineComponent, inject, ref, watch } from "vue";

export default defineComponent({
  name: "BasicTableToolbar",
  props: {
    filter: {
      type: String,
      required: true,
    },
    rowsPerPage: {
      type: Number,
      required: true,
    },
    editable: {
      type: Boolean,
      required: false,
      default: false,
    },
    title: {
      type: String,
      required: true,
    },
  },
  components: {
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  emits: ["changeRowsPerPage", "changeFilter", "changeEditMode"],
  setup(props, context) {
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
    const filterValue = ref(props.filter);
    const isEditModeOn = ref(false);

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

    const onChangeFilterValue = (value) => {
      filterValue.value = value;
      context.emit("changeFilter", value);
    };

    watch(isEditModeOn, (newValue) => {
      context.emit("changeEditMode", newValue);
    });

    return {
      context,
      columns,
      filterValue,
      isEditModeOn,
      onChangeColumnVisibility,
      onChangeFilterValue,
      onChangeRowsPerPageValue,
      rowsPerPageOptions,
      rowsPerPageValue,
      visibleColumns,
    };
  },
});
</script>
