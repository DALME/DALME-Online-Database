<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
        :title="title"
        :rows="rows"
        :columns="columns"
        :no-data-label="noData"
        :filter="filter"
        :title-class="{ 'text-h6': true }"
        :loading="loading"
        @request="onRequest"
        v-model:pagination="pagination"
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

        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <router-link
              class="text-subtitle2"
              :to="{ name: 'Set', params: { objId: props.row.id } }"
            >
              {{ props.value }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-owner="props">
          <q-td :props="props">
            <router-link
              :to="{
                name: 'User',
                params: { username: props.value.username },
              }"
            >
              {{ props.value.fullName }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-hasLanding="props">
          <q-td :props="props">
            <q-icon :name="props.value ? 'done' : 'close'" />
          </q-td>
        </template>

        <template v-slot:body-cell-endpoint="props">
          <q-td :props="props">
            <q-badge outline color="primary" label="Outline">
              {{ props.value }}
            </q-badge>
          </q-td>
        </template>

        <template v-slot:body-cell-permissions="props">
          <q-td :props="props">
            {{ props.value.name }}
          </q-td>
        </template>
      </q-table>
      <OpaqueSpinner :showing="loading" />
    </q-card>
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { keys, map } from "ramda";
import { defineComponent, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
import { setListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";

import { columnsByType } from "./columns";

export default defineComponent({
  name: "Sets",
  components: {
    OpaqueSpinner,
  },
  setup(_, context) {
    const $route = useRoute();
    const { loading, success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const rows = ref([]);
    const setType = ref("");
    const setTypeAPI = ref("");
    const title = ref("");

    useMeta(() => ({ title: title.value }));

    const noData = "No sets found.";
    const setMap = { corpora: 1, collections: 2, datasets: 3, worksets: 4 };

    const getColumns = () => {
      const columnMap = columnsByType(setType.value);
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys(columnMap));
    };

    const fetchData = async (query) => {
      const setTypeConstant = setMap[setTypeAPI.value];
      const request = requests.sets.getSets(setTypeConstant, query);
      const schema = setListSchema(setType.value);
      await fetchAPI(request);
      if (success.value)
        await schema
          .validate(data.value.data, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns();
            pagination.value.rowsNumber = value.count;
            rows.value.splice(0, rows.value.length, ...value);
            loading.value = false;
          });
    };

    const {
      fetchDataPaginated,
      filter,
      pagination,
      onRequest,
      resetPagination,
    } = usePagination(fetchData);

    onBeforeRouteLeave(() => {
      if (loading.value) return false;
    });

    watch(
      () => $route.name,
      async (to) => {
        const reload = ["Corpora", "Collections", "Datasets", "Worksets"];
        const reloadPage = async () => {
          loading.value = true;
          setTypeAPI.value = $route.meta.setTypeAPI;
          setType.value = $route.meta.setType;
          const setTitle = () => (title.value = to);
          let updateTitle = true;
          if (!title.value) {
            setTitle();
            updateTitle = false;
          }
          resetPagination();
          await fetchDataPaginated();
          if (updateTitle) setTitle();
        };
        if (reload.includes(to)) {
          await reloadPage();
        }
      },
      { immediate: true },
    );

    return {
      columns,
      filter,
      loading,
      noData,
      onRequest,
      pagination,
      rows,
      title,
    };
  },
});
</script>
