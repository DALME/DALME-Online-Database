<template>
  <BasicTable
    :columns="columns"
    :filter="filter"
    :loading="loading"
    :noData="noData"
    :onChangeFilter="onChangeFilter"
    :onChangePage="onChangePage"
    :onChangeRowsPerPage="onChangeRowsPerPage"
    :onRequest="onRequest"
    :pagination="pagination"
    :rows="rows"
    :title="title"
    :visibleColumns="visibleColumns"
  >
    <template v-slot:render-cell-name="props">
      <router-link
        class="text-subtitle2 text-link"
        :to="{ name: 'Set', params: { id: props.row.id } }"
      >
        {{ props.row.name }}
      </router-link>
    </template>

    <template v-slot:render-cell-owner="props">
      <router-link
        class="text-link"
        :to="{ name: 'User', params: { username: props.row.owner.username } }"
      >
        {{ props.row.owner.fullName }}
      </router-link>
    </template>

    <template v-slot:render-cell-isPublic="props">
      <BooleanIcon
        :value="props.row.isPublic"
        :onlyTrue="true"
        trueIcon="public"
      />
    </template>

    <template v-slot:render-cell-hasLanding="props">
      <BooleanIcon
        :value="props.row.hasLanding"
        :onlyTrue="true"
        trueIcon="check_circle"
      />
    </template>

    <template v-slot:render-cell-endpoint="props">
      <q-badge color="blue-grey-1" text-color="blue-grey-7" class="wf-tag">
        {{ props.row.endpoint }}
      </q-badge>
    </template>

    <template v-slot:render-cell-permissions="props">
      {{ props.row.permissions.name }}
    </template>

    <template v-slot:render-cell-datasetUsergroup="props">
      {{ props.row.datasetUsergroup.name }}
    </template>
  </BasicTable>
</template>

<script>
import { useMeta } from "quasar";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { requests } from "@/api";
import { BasicTable } from "@/components";
import { BooleanIcon, getColumns, getDefaults } from "@/components/utils";
import { setListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { columnsByType } from "./columns";

export default defineComponent({
  name: "Sets",
  components: {
    BasicTable,
    BooleanIcon,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const setType = ref("");
    const setTypeAPI = ref("");
    const title = ref("");

    useMeta(() => ({ title: title.value }));

    const columnMap = computed(() => {
      return columnsByType($route.meta.setType);
    });

    const noData = "No sets found.";
    const setMap = { corpora: 1, collections: 2, datasets: 3, worksets: 4 };

    const fetchData = async (query) => {
      const setTypeConstant = setMap[setTypeAPI.value];
      const request = requests.sets.getSetsByType(setTypeConstant, query);
      const schema = setListSchema(setType.value);
      await fetchAPI(request);
      if (success.value)
        await schema
          .validate(data.value.data, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns(columnMap.value);
            pagination.value.rowsNumber = data.value.recordsFiltered;
            pagination.value.rowsTotal = data.value.recordsTotal;
            rows.value.splice(0, rows.value.length, ...value);
            loading.value = false;
          });
    };

    const {
      fetchDataPaginated,
      filter,
      onChangeFilter,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      pagination,
      resetPagination,
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap.value));

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);

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
      onChangeFilter,
      onChangePage,
      onChangeRowsPerPage,
      onRequest,
      pagination,
      rows,
      title,
      visibleColumns,
    };
  },
});
</script>
