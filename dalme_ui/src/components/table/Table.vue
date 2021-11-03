<template>
  <q-card class="q-ma-md" v-bind:class="{ dirty: isDirty }">
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
            :key="column.field"
            :props="props"
            v-bind:class="{
              'text-red-6': isDirty && cellIsDirty(props.row.id, column.field),
            }"
          >
            {{ props.row[column.field] }}

            <template v-if="editable.includes(column.field)">
              <q-popup-edit
                v-model="props.row[column.field]"
                v-slot="scope"
                :validate="validation[schemaTypes[column.field]]"
                @before-show="
                  editError = false;
                  editErrorMessage = '';
                "
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
    <TransportSubmit v-if="isDirty" @submit-transport="handleSubmitTransport" />
    <OpaqueSpinner :showing="loading || saving" />
  </q-card>
</template>

<script>
import { mapObjIndexed } from "ramda";
import { defineComponent, inject, provide, ref } from "vue";
import { onBeforeRouteLeave } from "vue-router";

import { TransportSubmit } from "@/components";
import { OpaqueSpinner } from "@/components/utils";
import { useAPI, useNotifier, useTransport } from "@/use";

export default defineComponent({
  name: "Table",
  components: {
    OpaqueSpinner,
    TransportSubmit,
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
      required: true,
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
      type: Function,
      required: true,
    },
    updateRequest: {
      type: Function,
      required: true,
    },
  },
  setup(props, context) {
    const $notifier = useNotifier();
    const {
      isDirty,
      cellIsDirty,
      objDiffs,
      onDiff,
      resetTransport,
      transportWatcher,
    } = useTransport();

    const filter = ref("");
    const enableSave = ref(false);
    const saving = ref(false);
    const rows = inject("rows");

    // Can only open one popup at a time so we can share these.
    const editError = ref(false);
    const editErrorMessage = ref("");

    const schemaTypes = mapObjIndexed(
      (val) => val.type,
      props.schema.innerType.fields,
    );

    const isNumber = (val) => !isNaN(parseFloat(val)) && isFinite(val);
    const validation = {
      number: (val) => {
        if (!isNumber(val)) {
          editError.value = true;
          editErrorMessage.value = "Input must be a number.";
          return false;
        }
        editError.value = false;
        editErrorMessage.value = "";
        return true;
      },
      string: (val) => {
        if (val.length === 0) {
          editError.value = true;
          editErrorMessage.value = "Enter a value.";
          return false;
        }
        editError.value = false;
        editErrorMessage.value = "";
        return true;
      },
    };

    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

    provide("enableSave", enableSave);

    transportWatcher(rows);

    const handleSubmitTransport = async () => {
      saving.value = true;
      const { success, status, fetchAPI } = useAPI(context);
      const request = props.updateRequest(objDiffs);
      await fetchAPI(request);
      if (success.value && status.value == 201) {
        $notifier.CRUD.inlineUpdateSuccess(props.title);
        resetTransport();
        await props.fetchData();
      } else {
        $notifier.CRUD.inlineUpdateFailed(props.title);
        enableSave.value = true;
      }
      saving.value = false;
    };

    onBeforeRouteLeave(() => resetTransport());

    return {
      cellIsDirty,
      editError,
      editErrorMessage,
      filter,
      handleSubmitTransport,
      isDirty,
      onDiff,
      pagination,
      rows,
      saving,
      schemaTypes,
      validation,
    };
  },
});
</script>
