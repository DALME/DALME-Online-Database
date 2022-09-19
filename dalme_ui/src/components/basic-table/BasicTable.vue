<template>
  <div class="q-pa-md full-width full-height">
    <q-card
      flat
      bordered
      class="detail-card"
      v-bind:class="
        editable && isAdmin
          ? {
              focussed: isFocussed,
              pulse: mouseoverSubmit && isFocussed,
            }
          : null
      "
    >
      <BasicTableToolbar
        :title="title"
        :filter="filter"
        :rowsPerPage="pagination.rowsPerPage"
        :editable="!isEmpty(editable)"
        @changeRowsPerPage="onChangeRowsPerPage"
        @changeFilter="onChangeFilter"
        @changeEditMode="onChangeEditMode"
      />
      <q-separator class="bg-indigo-3" />
      <q-table
        flat
        wrap-cells
        :rows="rows"
        :columns="columns"
        :visible-columns="visibleColumns"
        :no-data-label="noData"
        :filter="filter"
        :loading="loading"
        @request="onRequest"
        v-model:pagination="pagination"
        row-key="id"
        class="basic-list"
        table-header-class="bg-grey-2"
        table-header-style="height: 35px"
      >
        <template v-slot:bottom="scope">
          <BasicTablePager :scope="scope" @changePage="onChangePage" />
        </template>

        <template v-slot:header-cell="props">
          <th style="padding: 0">
            <q-item
              dense
              style="height: 35px; padding-right: 10px"
              :class="
                editMode && editable.includes(props.col.name)
                  ? `bg-red-1 ${props.col.headerClasses}`
                  : props.col.headerClasses
              "
            >
              <q-item-section class="text-left">
                {{ props.col.label }}
              </q-item-section>
              <q-item-section
                v-if="isAdmin && editable.includes(props.col.name)"
                side
              >
                <q-icon
                  name="edit"
                  size="xs"
                  :color="editMode ? 'red-4' : 'grey-5'"
                />
              </q-item-section>
              <q-item-section
                v-if="props.col.sortable"
                side
                style="padding-left: 2px"
              >
                <q-btn
                  flat
                  dense
                  stack
                  size="sm"
                  style="height: 25px; width: 23px"
                  @click="sort(props.col.name)"
                >
                  <q-icon
                    name="arrow_drop_up"
                    size="sm"
                    style="height: 9px; width: 16px"
                    :color="
                      pagination.sortBy === props.col.name &&
                      !pagination.sortDesc
                        ? 'indigo-5'
                        : 'grey-5'
                    "
                  />
                  <q-icon
                    v-if="props.col.sortable"
                    name="arrow_drop_down"
                    size="sm"
                    style="height: 9px; width: 16px"
                    :color="
                      pagination.sortBy === props.col.name &&
                      pagination.sortDesc
                        ? 'indigo-5'
                        : 'grey-5'
                    "
                  />
                </q-btn>
              </q-item-section>
            </q-item>
          </th>
        </template>

        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td
              v-for="column in columns"
              v-bind:class="
                isAdmin
                  ? {
                      'text-red-6':
                        isDirty && cellIsDirty(props.row.id, column.field),
                      'bg-green-1':
                        submitting && cellIsDirty(props.row.id, column.field),
                    }
                  : null
              "
              :key="column.field"
              :auto-width="column.autoWidth"
              :props="props"
            >
              <slot :name="`render-cell-${column.field}`" v-bind="props">
                <template v-if="isObj(props.row[column.field])">
                  {{ props.row[column.field].name }}
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
                  :validate="getValidation(column.field)"
                  @before-show="clearError"
                  @save="
                    (value, prev) =>
                      onDiff(props.row.id, column.field, value, prev)
                  "
                  buttons
                >
                  <q-input
                    :type="
                      schemaTypes[column.field] === 'string'
                        ? 'text'
                        : schemaTypes[column.field]
                    "
                    :error="editError"
                    :error-message="editErrorMessage"
                    :step="/\D/.test(props.row[column.field]) ? '0.01' : '1'"
                    v-model="scope.value"
                    @keyup.enter="scope.set"
                    dense
                    counter
                    autofocus
                  />
                </q-popup-edit>
              </template>
            </q-td>
          </q-tr>
        </template>
      </q-table>
      <OpaqueSpinner :showing="loading || submitting" />
    </q-card>
  </div>
</template>

<script>
import { isEmpty, keys, map, mapObjIndexed } from "ramda";
import { computed, defineComponent, inject, ref, watch } from "vue";
import { OpaqueSpinner } from "@/components/utils";
import BasicTableToolbar from "./BasicTableToolbar.vue";
import BasicTablePager from "./BasicTablePager.vue";
import { onBeforeRouteLeave } from "vue-router";
import { useActor } from "@xstate/vue";
import { useAPI, useEditing, usePermissions, useTransport } from "@/use";

export default defineComponent({
  name: "BasicTable",
  components: {
    BasicTableToolbar,
    OpaqueSpinner,
    BasicTablePager,
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
    filter: {
      type: String,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    noData: {
      type: String,
      required: true,
    },
    onChangeFilter: {
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
    title: {
      type: String,
      required: true,
    },
    updateRequest: {
      type: Function,
      required: false,
    },
    visibleColumns: {
      type: Array,
      required: true,
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

    const {
      permissions: { isAdmin },
    } = usePermissions();

    const {
      diffCount,
      isDirty,
      cellIsDirty,
      objDiffs,
      onDiff,
      resetTransport,
      transportWatcher,
    } = useTransport();

    // We can only open one inline popup at a time when doing editing, so we
    // can share these, no need for any scoping/duplication etc.
    const editError = ref(false);
    const editErrorMessage = ref("");
    const editMode = ref(false);

    const isNumber = (val) => !isNaN(parseFloat(val)) && isFinite(val);
    const isObj = (obj) => {
      const type = typeof obj;
      return type === "function" || (type === "object" && !!obj);
    };

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
      number: [
        { check: (val) => !isNumber(val), error: "Input must be a number." },
      ],
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
        actorSend.value("RESOLVE");
        resetTransport();
        await props.fetchData();
      } else {
        actorSend.value("REJECT");
      }
    };

    const isFocussed = computed(() => inline.value && focus.value === "inline");

    const sort = (value) => {
      if (value === pagination.value.sortBy) {
        pagination.value.sortDesc = !pagination.value.sortDesc;
      } else {
        pagination.value.sortBy = value;
        pagination.value.sortDesc = props.columns[value]["sortOrder"] === "da";
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

    watch(
      () => diffCount.value,
      (count, prevCount) => {
        if (prevCount === 0 && count === 1) {
          send("SPAWN_INLINE");
          const actor = useActor(inline.value);
          actorSend.value = actor.send;
          formSubmitWatcher(actor.state, handleSubmit);
          showEditing.value(); // Open the edit panel.
        }
        if (prevCount === 1 && count === 0) {
          send("DESTROY_INLINE");
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
      focus,
      getValidation,
      handleSubmit,
      inline,
      isAdmin,
      isDirty,
      isEmpty,
      isFocussed,
      isObj,
      mouseoverSubmit,
      onChangeEditMode,
      onDiff,
      pagination,
      schemaTypes,
      sort,
      submitting,
    };
  },
});
</script>

<style lang="scss" scoped>
.focussed {
  border: 2px solid green;
  transition: border 0.05s linear;
}
.pulse {
  border: 2px solid red;
  border-radius: 0;
  transition: border 0.5s linear;
  transition: border-radius 0.5s linear;
}
</style>
