<template>
  <DataTable
    :columns="columns"
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
    use-expansion
  >
    <template #grid-avatar>
      <q-icon color="grey-5" name="mdi-archive" size="22px" />
    </template>

    <template #grid-main="props">
      <DetailPopover
        :link-target="{ name: 'Record Group', params: { id: props.row.id } }"
        :link-text="props.row.shortName"
        link-class="text-h7 title-link"
      >
        <div class="text-h8 q-mb-xs">
          {{ props.row.shortName }}
        </div>
      </DetailPopover>
      <TagPill
        v-if="props.row.isPrivate"
        class="q-ml-sm"
        colour="deep-orange-1"
        module="standalone"
        name="private"
        size="xs"
        text-colour="deep-orange-8"
      />
    </template>

    <template #grid-detail="props">
      <span class="text-detail text-weight-medium text-grey-8">
        {{ props.row.name }} | {{ props.row.id }}
      </span>
    </template>

    <template #grid-counter="props">
      <q-icon
        v-if="props.row.noRecords"
        class="text-weight-bold q-mr-xs"
        name="o_import_contacts"
        size="17px"
      />
      <div class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.noRecords }}
      </div>
    </template>

    <template #grid-counter-extra="props">
      <q-icon
        v-if="props.row.workflow"
        class="text-weight-bold q-mr-xs"
        color="red-4"
        name="flag"
        size="17px"
      />
    </template>

    <template #render-cell-name="props">
      <router-link
        :to="{ name: 'Record', params: { id: props.row.id } }"
        class="text-subtitle2 text-link"
      >
        {{ props.row.name }}
      </router-link>
    </template>

    <template #render-cell-owner="props">
      <router-link
        :to="{
          name: 'User',
          params: { username: props.row.owner.username },
        }"
        class="text-link"
      >
        {{ props.row.owner.fullName }}
      </router-link>
    </template>

    <template #render-cell-activity="props">
      <span>
        <router-link
          :to="{
            name: 'User',
            params: { username: props.row.workflow.lastUser.username },
          }"
          class="text-link"
        >
          {{ props.row.workflow.lastUser.fullName }}
        </router-link>
        <br />
        {{ props.row.workflow.lastModified }}
      </span>
    </template>

    <template #render-cell-isPrivate="props">
      <BooleanValue
        :only-true="true"
        :only-true-green="false"
        :value="props.row.isPrivate"
        true-icon="lock"
      />
    </template>
  </DataTable>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide, ref } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

import { requests } from "@/api";
import { BooleanValue, DataTable, DetailPopover, TagPill } from "@/components";
import { recordGroupListSchema } from "@/schemas";
import { useAPI, usePagination, useStores } from "@/use";
import { getColumns, getDefaults } from "@/utils";

import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

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
