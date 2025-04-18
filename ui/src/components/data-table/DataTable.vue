<template>
  <div class="q-pb-lg q-pt-xs full-width full-height">
    <TableToolbar
      @change-edit-mode="onChangeEditMode"
      @change-filters="onChangeFilters"
      @change-rows-per-page="onChangeRowsPerPage"
      @change-search="onChangeSearch"
      @change-sort="onChangeSort"
      @clear-filters="onClearFilters"
      :editable="!isEmpty(editable)"
      :embedded="embedded"
      :filter-list="filterList"
      :grid="grid"
      :resource="resource"
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
              :class="
                editMode && editable.includes(props.col.name)
                  ? `bg-red-1 ${props.col.headerClasses}`
                  : props.col.headerClasses
              "
              style="height: 35px; padding-right: 10px"
              dense
            >
              <q-item-section class="text-left">
                {{ props.col.label }}
              </q-item-section>
              <q-item-section v-if="isAdmin && editable.includes(props.col.name)" side>
                <q-icon :color="editMode ? 'red-4' : 'grey-5'" name="edit" size="xs" />
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
              :class="
                isAdmin
                  ? {
                      'text-red-6': isDirty && cellIsDirty(props.row.id, column.field),
                      'bg-green-1': submitting && cellIsDirty(props.row.id, column.field),
                    }
                  : null
              "
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

              <template v-if="isAdmin && editable.includes(column.field)">
                <q-popup-edit
                  v-if="editMode"
                  v-model="props.row[column.field]"
                  v-slot="scope"
                  @before-show="clearError"
                  @save="(value, prev) => onDiff(props.row.id, column.field, value, prev)"
                  :validate="getValidation(column.field)"
                  buttons
                >
                  <q-input
                    v-model="scope.value"
                    @keyup.enter="scope.set"
                    :error="editError"
                    :error-message="editErrorMessage"
                    :step="/\D/.test(props.row[column.field]) ? '0.01' : '1'"
                    :type="
                      schemaTypes[column.field] === 'string' ? 'text' : schemaTypes[column.field]
                    "
                    autofocus
                    counter
                    dense
                  />
                </q-popup-edit>
              </template>
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
      <OpaqueSpinner :showing="loading || submitting" />
    </q-card>
  </div>
</template>

<script>
import { useActor } from "@xstate/vue";
import { isEmpty, keys, map, mapObjIndexed } from "ramda";
import { computed, defineComponent, inject, provide, ref, watch } from "vue";
import { onBeforeRouteLeave } from "vue-router";

import { OpaqueSpinner } from "@/components";
import { useAPI, useEditing, useStores, useTransport } from "@/use";
import { isNumber, isObject } from "@/utils";

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
    const { apiInterface } = useAPI();
    const { pagination, fetchDataPaginated } = inject("pagination");

    const {
      focus,
      formSubmitWatcher,
      inline,
      mouseoverSubmit,
      showEditing,
      submitting,
      machine: { send },
    } = useEditing();

    const { auth } = useStores();

    const { diffCount, isDirty, cellIsDirty, objDiffs, onDiff, resetTransport, transportWatcher } =
      useTransport();

    // We can only open one inline popup at a time when doing editing, so we
    // can share these, no need for any scoping/duplication etc.
    const editError = ref(false);
    const editErrorMessage = ref("");
    const editMode = ref(false);

    const expanded = ref(props.columns.map((value) => value.id));

    const schemaTypes = () => {
      if (props.schema) {
        mapObjIndexed((val) => val.type, props.schema.innerType.fields);
      }
    };

    // The generic validation will be applied to all editable columns but
    // if you need further checks then provide the fieldValidation prop using
    // the same format and they will be picked up in turn. For example, in some
    // component that called Table.vue:
    //   const fieldValidation = {
    //     fieldName: [
    //       { check: (val) => val.includes("zzz"), error: "No snoozing!" },
    //       { check: (val) => val.includes("ZZZ"), error: "No snoring!" },
    //     ],
    //   };
    const genericValidation = {
      number: [{ check: (val) => !isNumber(val), error: "Input must be a number." }],
      // TODO: Disabled this check so the place.notes field can be nulled
      // (which is the only inline editable field currently in use). We need to
      // develop a better, nullable solution for this system, but it's not in
      // budget right now.
      // string: [{ check: (val) => val.length === 0, error: "Enter a value." }],
    };

    const clearError = () => {
      editError.value = false;
      editErrorMessage.value = "";
    };

    const getValidation = (field) => {
      const fieldValidators = keys(props.fieldValidation);
      let validators = genericValidation[schemaTypes[field]];
      if (props.fieldValidation && fieldValidators.includes(field)) {
        validators = [...validators, ...props.fieldValidation[field]];
      }
      return (val) => {
        const validated = map(
          (validator) => (validator.check(val) ? validator.error : ""),
          validators,
        ).filter(Boolean);
        if (validated.length) {
          editError.value = true;
          editErrorMessage.value = validated.join("\n");
          return false;
        }
        clearError();
        return true;
      };
    };

    const actorSend = ref(null);
    const handleSubmit = async () => {
      const { success, status, fetchAPI } = apiInterface();
      const request = props.updateRequest(objDiffs);
      await fetchAPI(request);
      if (success.value && status.value == 201) {
        actorSend.value({ type: "RESOLVE" });
        resetTransport();
        await props.fetchData();
      } else {
        actorSend.value({ type: "REJECT" });
      }
    };

    const isFocussed = computed(() => inline.value && focus.value === "inline");

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

    const onChangeEditMode = (value) => {
      if (value) {
        editMode.value = true;
      } else {
        // if there is unsaved data, show dialogue
        // save or delete
        editMode.value = false;
      }
    };

    const showGrid = ref(props.grid);
    provide("showGrid", showGrid);

    watch(
      () => diffCount.value,
      (count, prevCount) => {
        if (prevCount === 0 && count === 1) {
          send({ type: "SPAWN_INLINE" });
          const actor = useActor(inline.value);
          actorSend.value = actor.send;
          formSubmitWatcher(actor.state, handleSubmit);
          showEditing.value(); // Open the edit panel.
        }
        if (prevCount === 1 && count === 0) {
          send({ type: "DESTROY_INLINE" });
        }
      },
    );

    transportWatcher(props.rows);

    onBeforeRouteLeave(() => {
      resetTransport();
    });

    return {
      cellIsDirty,
      clearError,
      editError,
      editErrorMessage,
      editMode,
      expanded,
      focus,
      getValidation,
      handleSubmit,
      inline,
      isAdmin: auth.user.isAdmin,
      isDirty,
      isEmpty,
      isFocussed,
      isObject,
      mouseoverSubmit,
      onChangeEditMode,
      onChangeSort,
      onDiff,
      pagination,
      schemaTypes,
      showGrid,
      submitting,
    };
  },
});
</script>

<style lang="scss" scoped>
.basic-list .q-table__bottom {
  min-height: 35px;
  padding: 0;
  background: #fafafa;
  border-top: none;
}
.basic-list .q-table__bottom--nodata {
  padding-left: 12px;
}
.basic-list th {
  padding: 0;
  border-right: 1px dotted rgb(209, 209, 209);
}
.basic-list table {
  border-bottom: none;
}
.basic-list thead > tr > th:last-of-type {
  border-right: none;
}
.basic-list.q-table--grid .q-table__middle {
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
