<template>
  <DataTable
    grid
    :columns="columns"
    :embedded="embedded"
    :search="search"
    :filterList="filterList"
    :loading="loading"
    :noData="noData"
    :onChangeSearch="onChangeSearch"
    :onChangePage="onChangePage"
    :onChangeRowsPerPage="onChangeRowsPerPage"
    :onChangeFilters="onChangeFilters"
    :onClearFilters="onClearFilters"
    :onRequest="onRequest"
    :pagination="pagination"
    :rows="rows"
    :sortList="sortList"
    :title="title"
    :visibleColumns="visibleColumns"
  >
    <template v-slot:toolbar-filtersets>
      <GeneralChooser showSelected type="users" label="Author" @clear-filters="onClearFilters" />
      <GeneralChooser showSelected type="users" label="Assignee" @clear-filters="onClearFilters" />
    </template>

    <template v-slot:grid-avatar="props">
      <q-icon name="check_circle_outline" color="purple-8" size="22px" :test="props.row.setType" />
    </template>

    <template v-slot:grid-main="props">
      <DetailPopover
        linkClass="text-h7 title-link"
        :linkTarget="{ name: 'Set', params: { id: props.row.id } }"
        :linkText="props.row.name"
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

    <template v-slot:grid-detail="props">
      <div class="text-detail text-weight-medium text-grey-8">
        {{ props.row.detailString }}
      </div>
    </template>

    <template v-slot:grid-counter="props">
      <q-icon name="chat_bubble_outline" size="17px" class="text-weight-bold q-mr-xs" />
      <div class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.memberCount }}
      </div>
    </template>

    <template v-slot:grid-counter-extra="props">
      <q-icon name="chat_bubble_outline" size="17px" class="text-weight-bold q-mr-xs" />
      <div class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.publicMemberCount }}
      </div>
    </template>

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
      <BooleanValue :value="props.row.isPublic" :onlyTrue="true" trueIcon="public" />
    </template>

    <template v-slot:render-cell-hasLanding="props">
      <BooleanValue :value="props.row.hasLanding" :onlyTrue="true" trueIcon="check_circle" />
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
  </DataTable>
</template>

<script>
import { useMeta } from "quasar";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { requests } from "@/api";
import { BooleanValue, GeneralChooser, DataTable, DetailPopover } from "@/components";
import { formatDate, getColumns, getDefaults } from "@/utils";
import { setListSchema } from "@/schemas";
import { useAPI, usePagination, useStores } from "@/use";
import { columnsByType } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "SetList",
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    GeneralChooser,
    DataTable,
    BooleanValue,
    DetailPopover,
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
        ? requests.sets.getUserWorksets(auth.user.userId)
        : requests.sets.getSetsByType(setTypeConstant, query);
      const schema = setListSchema(setType.value);
      await fetchAPI(request);
      if (success.value)
        await schema.validate(data.value.data, { stripUnknown: true }).then((value) => {
          columns.value = getColumns(columnMap.value);
          pagination.value.rowsNumber = data.value.filtered;
          pagination.value.rowsTotal = data.value.count;
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
      filterList: filterList(auth.user.userId),
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
