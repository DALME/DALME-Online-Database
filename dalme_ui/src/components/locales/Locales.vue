<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md" v-bind:class="{ dirty: isDirty }">
      <q-table
        :title="title"
        :rows="rows"
        :columns="columns"
        :no-data-label="noData"
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
              key="name"
              :props="props"
              v-bind:class="{
                'text-red-6': isDirty && cellIsDirty(props.row.id, 'name'),
              }"
            >
              {{ props.row.name }}
              <q-popup-edit
                v-model="props.row.name"
                v-slot="scope"
                @save="
                  (value, prev) => onDiff(props.row.id, 'name', value, prev)
                "
                buttons
              >
                <q-input
                  dense
                  counter
                  autofocus
                  v-model="scope.value"
                  @keyup.enter="scope.set"
                />
              </q-popup-edit>
            </q-td>

            <q-td
              key="administrativeRegion"
              :props="props"
              v-bind:class="{
                'text-red-6':
                  isDirty && cellIsDirty(props.row.id, 'administrativeRegion'),
              }"
            >
              {{ props.row.administrativeRegion }}
              <q-popup-edit
                v-model="props.row.administrativeRegion"
                v-slot="scope"
                @save="
                  (value, prev) =>
                    onDiff(props.row.id, 'administrativeRegion', value, prev)
                "
                buttons
              >
                <q-input
                  dense
                  counter
                  autofocus
                  v-model="scope.value"
                  @keyup.enter="scope.set"
                />
              </q-popup-edit>
            </q-td>

            <q-td key="country" :props="props">
              {{ props.row.country.name }}
            </q-td>

            <q-td
              key="latitude"
              :props="props"
              v-bind:class="{
                'text-red-6': isDirty && cellIsDirty(props.row.id, 'latitude'),
              }"
            >
              {{ props.row.latitude }}
              <q-popup-edit
                v-model="props.row.latitude"
                v-slot="scope"
                @save="
                  (value, prev) => onDiff(props.row.id, 'latitude', value, prev)
                "
                buttons
              >
                <q-input
                  dense
                  counter
                  autofocus
                  v-model="scope.value"
                  @keyup.enter="scope.set"
                />
              </q-popup-edit>
            </q-td>

            <q-td
              key="longitude"
              :props="props"
              v-bind:class="{
                'text-red-6': isDirty && cellIsDirty(props.row.id, 'longitude'),
              }"
            >
              {{ props.row.longitude }}
              <q-popup-edit
                v-model="props.row.longitude"
                v-slot="scope"
                @save="
                  (value, prev) =>
                    onDiff(props.row.id, 'longitude', value, prev)
                "
                buttons
              >
                <q-input
                  dense
                  counter
                  autofocus
                  v-model="scope.value"
                  @keyup.enter="scope.set"
                />
              </q-popup-edit>
            </q-td>
          </q-tr>
        </template>
      </q-table>
      <TransportSubmit
        v-if="isDirty"
        @submit-transport="handleSubmitTransport"
      />
      <OpaqueSpinner :showing="loading" />
    </q-card>
  </div>
</template>

<script>
import { map, keys } from "ramda";
import { defineComponent, onMounted, provide, ref } from "vue";

import { requests } from "@/api";
import { TransportSubmit } from "@/components";
import { OpaqueSpinner } from "@/components/utils";
import { localeListSchema } from "@/schemas";
import { useAPI, useNotifier, useTransport } from "@/use";

const columnMap = {
  name: "Name",
  administrativeRegion: "Administrative Region",
  country: "Country",
  latitude: "Latitude",
  longitude: "Longitude",
};

export default defineComponent({
  name: "Locales",
  components: {
    OpaqueSpinner,
    TransportSubmit,
  },
  setup(_, context) {
    const $notifier = useNotifier();
    const { loading, success, data, fetchAPI } = useAPI(context);
    const {
      isDirty,
      cellIsDirty,
      objDiffs,
      onDiff,
      resetTransport,
      transportWatcher,
    } = useTransport();

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");
    const enableSave = ref(false);

    provide("enableSave", enableSave);

    const noData = "No locales found.";
    const title = "Locales";
    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

    const getColumns = () => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys(columnMap));
    };

    transportWatcher(rows);

    const handleSubmitTransport = async () => {
      const request = requests.locales.updateLocales(objDiffs);
      const {
        success: editSuccess,
        status: editStatus,
        fetchAPI: editFetchAPI,
      } = useAPI(context);
      await editFetchAPI(request);
      if (editSuccess.value && editStatus.value == 201) {
        $notifier.CRUD.inlineUpdateSuccess("Locales");
        resetTransport();
        await fetchData();
      } else {
        $notifier.CRUD.inlineUpdateFailed("Locales");
        enableSave.value = true;
      }
    };

    const fetchData = async () => {
      const request = requests.locales.getLocales();
      await fetchAPI(request);
      if (success.value)
        await localeListSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns();
            rows.value = value;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    return {
      cellIsDirty,
      columns,
      filter,
      handleSubmitTransport,
      isDirty,
      loading,
      noData,
      onDiff,
      pagination,
      rows,
      title,
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
.dirty {
  border: 2px solid #f44336;
}
</style>
