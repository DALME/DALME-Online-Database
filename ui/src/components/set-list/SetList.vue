<template>
  <DataTable
    :columns="columns"
    :embedded="embedded"
    :filter-list="filterList"
    :loading="loading"
    :no-data="noData"
    :on-change-filters="onChangeFilters"
    :on-change-page="onChangePage"
    :on-change-rows-per-page="onChangeRowsPerPage"
    :on-change-search="onChangeSearch"
    :on-clear-filters="onClearFilters"
    :on-request="onRequest"
    :pagination="pagination"
    :rows="rows"
    :search="search"
    :sort-list="sortList"
    :title="title"
    :visible-columns="visibleColumns"
    grid
  >
    <template #toolbar-filtersets>
      <GeneralChooser @clear-filters="onClearFilters" label="Author" type="users" show-selected />
      <GeneralChooser @clear-filters="onClearFilters" label="Assignee" type="users" show-selected />
    </template>

    <template #grid-avatar="props">
      <q-icon :test="props.row.setType" color="purple-8" name="check_circle_outline" size="22px" />
    </template>

    <template #grid-main="props">
      <DetailPopover
        :link-target="{ name: 'Set', params: { id: props.row.id } }"
        :link-text="props.row.name"
        link-class="text-h7 title-link"
      >
        <div class="text-detail text-weight-medium text-grey-8 q-mb-sm">
          {{ props.row.owner.username }}
          {{ formatDate(props.row.creationTimestamp, false) }}
        </div>
        <div class="text-h8 q-mb-xs">
          {{ props.row.name }}
        </div>
        <div class="text-detail ellipsis-3-lines">
          {{ props.row.description }}
        </div>
      </DetailPopover>
    </template>

    <template #grid-detail="props">
      <div class="text-detail text-weight-medium text-grey-8">
        {{ props.row.detailString }}
      </div>
    </template>

    <template #grid-counter="props">
      <q-icon class="text-weight-bold q-mr-xs" name="chat_bubble_outline" size="17px" />
      <div class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.memberCount }}
      </div>
    </template>

    <template #grid-counter-extra="props">
      <q-icon class="text-weight-bold q-mr-xs" name="chat_bubble_outline" size="17px" />
      <div class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.publicMemberCount }}
      </div>
    </template>

    <template #render-cell-name="props">
      <router-link
        :to="{ name: 'Set', params: { id: props.row.id } }"
        class="text-subtitle2 text-link"
      >
        {{ props.row.name }}
      </router-link>
    </template>

    <template #render-cell-owner="props">
      <router-link
        :to="{ name: 'User', params: { username: props.row.owner.username } }"
        class="text-link"
      >
        {{ props.row.owner.fullName }}
      </router-link>
    </template>

    <template #render-cell-isPublic="props">
      <BooleanValue :only-true="true" :value="props.row.isPublic" true-icon="public" />
    </template>

    <template #render-cell-hasLanding="props">
      <BooleanValue :only-true="true" :value="props.row.hasLanding" true-icon="check_circle" />
    </template>

    <template #render-cell-endpoint="props">
      <q-badge class="wf-tag" color="blue-grey-1" text-color="blue-grey-7">
        {{ props.row.endpoint }}
      </q-badge>
    </template>

    <template #render-cell-permissions="props">
      {{ props.row.permissions.name }}
    </template>

    <template #render-cell-datasetUsergroup="props">
      {{ props.row.datasetUsergroup.name }}
    </template>
  </DataTable>
</template>

<script>
import { useMeta } from "quasar";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

import { requests } from "@/api";
import { BooleanValue, DataTable, DetailPopover, GeneralChooser } from "@/components";
import { setListSchema } from "@/schemas";
import { useAPI, usePagination, useStores } from "@/use";
import { formatDate, getColumns, getDefaults } from "@/utils";

import { columnsByType } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "SetList",
  components: {
    GeneralChooser,
    DataTable,
    BooleanValue,
    DetailPopover,
  },
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, context) {
    const $route = useRoute();
    const { auth } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const setType = ref("");
    const setTypeAPI = ref("");
    const title = props.embedded ? ref("My Worksets") : ref("");
    if (!props.embedded) useMeta({ title: title.value });
    const noData = props.embedded ? "No worksets created" : "No sets found.";

    const columnMap = computed(() => {
      const st = props.embedded ? "worksets" : $route.meta.setType;
      return columnsByType(st);
    });

    const setMap = { corpora: 1, collections: 2, datasets: 3, worksets: 4 };

    const fetchData = async (query) => {
      const setTypeConstant = setMap[setTypeAPI.value];
      // TODO: These set requests no longer exist.
      const request = props.embedded
        ? requests.sets.getUserWorksets(auth.user.id)
        : requests.sets.getSetsByType(setTypeConstant, query);
      const schema = setListSchema(setType.value);
      await fetchAPI(request);
      if (success.value)
        await schema.validate(data.value.data, { stripUnknown: true }).then((value) => {
          columns.value = getColumns(columnMap.value);
          pagination.value.rowsNumber = data.value.count;
          rows.value = value;
          //rows.value.splice(0, rows.value.length, ...value);
          loading.value = false;
        });
    };

    const {
      activeFilters,
      fetchDataPaginated,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      onRequest,
      pagination,
      search,
      resetPagination,
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap.value), props.embedded);

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);

    onBeforeRouteLeave(() => {
      if (loading.value) return false;
    });

    watch(
      () => $route.name,
      async (to) => {
        const reload = ["Corpora", "Collections", "Datasets", "Worksets"];
        if ($route.name == "Dashboard") {
          setTypeAPI.value = "worksets";
          setType.value = "worksets";
          resetPagination();
          await fetchDataPaginated();
        } else {
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

          if (reload.includes(to)) await reloadPage();
        }
      },
      { immediate: true },
    );

    return {
      context,
      columns,
      filterList: filterList(auth.user.id),
      formatDate,
      loading,
      noData,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      onRequest,
      pagination,
      rows,
      search,
      sortList: sortList(),
      title,
      visibleColumns,
    };
  },
});
</script>
