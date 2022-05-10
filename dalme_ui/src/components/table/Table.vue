<template>
  <q-card
    class="table q-ma-md"
    v-bind:class="
      isAdmin
        ? {
            focussed: isFocussed,
            pulse: mouseoverSubmit && isFocussed,
          }
        : null
    "
  >
    <q-table
      :title="title"
      :rows="rows"
      :columns="columns"
      :no-data-label="noDataLabel"
      :loading="loading"
      :filter="filter"
      :pagination="pagination"
      :title-class="{ 'text-h6': true }"
      row-key="id"
    >
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th
            v-for="column in props.cols"
            :key="column.name"
            :props="props"
            :style="{
              borderBottom:
                isAdmin && editable.includes(column.name)
                  ? '2px solid green'
                  : 'none',
            }"
          >
            {{ column.label }}

            <Tooltip v-if="isAdmin && editable.includes(column.name)">
              Click on fields in underlined columns to edit data in place.
            </Tooltip>
          </q-th>
        </q-tr>
      </template>

      <template v-slot:top-right>
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
            :props="props"
          >
            <template v-if="isObj(props.row[column.field])">
              {{ props.row[column.field].name }}
            </template>
            <template v-else>
              {{ props.row[column.field] }}
            </template>

            <template v-if="isAdmin && editable.includes(column.field)">
              <q-popup-edit
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
</template>

<script>
import { map, keys, mapObjIndexed } from "ramda";
import {
  computed,
  defineAsyncComponent,
  defineComponent,
  inject,
  ref,
  watch,
} from "vue";
import { onBeforeRouteLeave } from "vue-router";
import { useActor } from "@xstate/vue";

import { OpaqueSpinner } from "@/components/utils";
import { useAPI, useEditing, usePermissions, useTransport } from "@/use";

export default defineComponent({
  name: "Table",
  components: {
    OpaqueSpinner,
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  props: {
    // Reactive.
    columns: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    // Static.
    editable: {
      type: Array,
      default: () => [],
    },
    noDataLabel: {
      type: String,
      required: true,
    },
    schema: {
      type: Object,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    // Callbacks.
    fetchData: {
      required: true,
    },
    fieldValidation: {
      type: Object,
      required: false,
    },
    updateRequest: {
      type: Function,
      required: false,
    },
  },
  setup(props) {
    const { apiInterface } = useAPI();
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

    const rows = inject("rows");

    // We can only open one inline popup at a time when doing editing, so we
    // can share these, no need for any scoping/duplication etc.
    const editError = ref(false);
    const editErrorMessage = ref("");
    const filter = ref("");

    const isNumber = (val) => !isNaN(parseFloat(val)) && isFinite(val);
    const isObj = (obj) => {
      const type = typeof obj;
      return type === "function" || (type === "object" && !!obj);
    };

    const schemaTypes = mapObjIndexed(
      (val) => val.type,
      props.schema.innerType.fields,
    );

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
      string: [{ check: (val) => val.length === 0, error: "Enter a value." }],
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

    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

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

    transportWatcher(rows);

    onBeforeRouteLeave(() => {
      resetTransport();
    });

    return {
      cellIsDirty,
      clearError,
      editError,
      editErrorMessage,
      filter,
      focus,
      handleSubmit,
      inline,
      isAdmin,
      isDirty,
      isFocussed,
      isObj,
      mouseoverSubmit,
      onDiff,
      pagination,
      rows,
      submitting,
      schemaTypes,
      getValidation,
    };
  },
});
</script>

<style lang="scss" scoped>
.table {
  border: 0;
}
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
