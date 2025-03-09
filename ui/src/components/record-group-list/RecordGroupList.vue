<template>
  <DataTable
    grid
    useExpansion
    :columns="columns"
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
    <template v-slot:grid-avatar>
      <q-icon name="mdi-archive" color="grey-5" size="22px" />
    </template>

    <template v-slot:grid-main="props">
      <DetailPopover
        linkClass="text-h7 title-link"
        :linkTarget="{ name: 'Record Group', params: { id: props.row.id } }"
        :linkText="props.row.shortName"
      >
        <div class="text-h8 q-mb-xs">
          {{ props.row.shortName }}
        </div>
      </DetailPopover>
      <template>
        <TagPill
          v-if="props.row.isPrivate"
          name="private"
          colour="deep-orange-1"
          textColour="deep-orange-8"
          size="xs"
          module="standalone"
          class="q-ml-sm"
        />
      </template>
    </template>

    <template v-slot:grid-detail="props">
      <span class="text-detail text-weight-medium text-grey-8">
        {{ props.row.name }} | {{ props.row.id }}
      </span>
    </template>

    <template v-slot:grid-counter="props">
      <q-icon
        name="o_import_contacts"
        size="17px"
        v-if="props.row.noRecords"
        class="text-weight-bold q-mr-xs"
      />
      <div class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.noRecords }}
      </div>
    </template>

    <template v-slot:grid-counter-extra="props">
      <q-icon
        name="flag"
        size="17px"
        v-if="props.row.workflow"
        color="red-4"
        class="text-weight-bold q-mr-xs"
      />
    </template>

    <template v-slot:render-cell-name="props">
      <router-link
        class="text-subtitle2 text-link"
        :to="{ name: 'Record', params: { id: props.row.id } }"
      >
        {{ props.row.name }}
      </router-link>
    </template>

    <template v-slot:render-cell-owner="props">
      <router-link
        class="text-link"
        :to="{
          name: 'User',
          params: { username: props.row.owner.username },
        }"
      >
        {{ props.row.owner.fullName }}
      </router-link>
    </template>

    <template v-slot:render-cell-activity="props">
      <span>
        <router-link
          class="text-link"
          :to="{
            name: 'User',
            params: { username: props.row.workflow.lastUser.username },
          }"
        >
          {{ props.row.workflow.lastUser.fullName }}
        </router-link>
        <br />
        {{ props.row.workflow.lastModified }}
      </span>
    </template>

    <template v-slot:render-cell-isPrivate="props">
      <BooleanValue
        :value="props.row.isPrivate"
        :onlyTrue="true"
        :onlyTrueGreen="false"
        trueIcon="lock"
      />
    </template>
  </DataTable>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide, ref } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { requests } from "@/api";
import { getColumns, getDefaults } from "@/utils";
import { BooleanValue, DataTable, DetailPopover, TagPill } from "@/components";
import { useAPI, usePagination, useStores } from "@/use";
import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";
import { recordGroupListSchema } from "@/schemas";

export default defineComponent({
  name: "RecordGroupList",
  components: {
    BooleanValue,
    DetailPopover,
    DataTable,
    TagPill,
  },
  setup() {
    const $route = useRoute();
    const { auth } = useStores();
    const { currentPageIcon } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const title = ref("");

    useMeta(() => ({ title: title.value }));

    const noData = "No records found.";

    const getLanguage = (data) => {
      if (data.length > 1) {
        const langs = data.map((a) => a.name);
        return langs.join(", ");
      } else {
        return data[0].name;
      }
    };

    const fetchData = async (query) => {
      const request = requests.recordGroups.getRecordGroups(query);
      await fetchAPI(request);
      if (success.value)
        recordGroupListSchema.validate(data.value.data, { stripUnknown: false }).then((value) => {
          columns.value = getColumns(columnMap);
          pagination.value.rowsNumber = data.value.count;
          rows.value.splice(0, rows.value.length, ...value);
          loading.value = false;
        });
    };

    const setOwner = (value) => {
      onChangeFilters({
        field: "owner",
        value: value,
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
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap));

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);

    onBeforeRouteLeave(() => {
      if (loading.value) return false;
    });

    return {
      columns,
      currentPageIcon,
      getLanguage,
      filterList: filterList(auth.user.userId),
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
      setOwner,
    };
  },
});
</script>
