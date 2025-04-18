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
  >
    <template #grid-avatar="props">
      <q-avatar class="q-pt-xs" size="38px">
        <q-img v-if="!nully(props.row.avatar)" :src="props.row.avatar" fit="cover" ratio="1" />
        <q-icon v-else color="blue-grey-3" name="mdi-account-circle" size="40px" />
      </q-avatar>
    </template>

    <template #grid-main="props">
      <DetailPopover
        :link-target="{ name: 'User', params: { username: props.row.username } }"
        :link-text="props.row.fullName"
        link-class="text-h7 title-link"
      >
        <div class="text-h8 q-mb-xs">
          {{ props.row.username }}
        </div>
      </DetailPopover>
      <TagPill
        v-if="props.row.isActive"
        class="q-ml-sm"
        colour="light-green-1"
        module="standalone"
        name="active"
        size="xs"
        text-colour="light-green-9"
      />
      <TagPill
        v-if="props.row.isStaff"
        class="q-ml-sm"
        colour="light-blue-1"
        module="standalone"
        name="staff"
        size="xs"
        text-colour="light-blue-8"
      />
      <TagPill
        v-if="props.row.isSuperuser"
        class="q-ml-sm"
        colour="orange-1"
        module="standalone"
        name="super"
        size="xs"
        text-colour="orange-8"
      />
    </template>

    <template #grid-detail="props">
      <span class="text-detail text-weight-medium text-grey-8">
        #{{ props.row.id }} | {{ props.row.username }} |
        <a :href="`mailto:${props.row.email}`" class="text-link">
          {{ props.row.email }}
        </a>
      </span>
    </template>

    <template #grid-counter="props">
      <div class="text-detail text-weight-medium text-grey-8 q-ml-auto">
        Joined on {{ formatDate(props.row.dateJoined, "DATETIME_AT") }}
      </div>
    </template>

    <template #grid-counter-extra="props">
      <div class="text-detail text-weight-medium text-grey-8 q-ml-auto">
        Last active on {{ formatDate(props.row.lastLogin, "DATETIME_AT") }}
      </div>
    </template>

    <template #render-cell-username="props">
      <router-link
        :to="{ name: 'User', params: { username: props.row.username } }"
        class="text-link"
      >
        {{ props.row.username }}
      </router-link>
    </template>

    <template #render-cell-id="props">
      {{ props.row.id }}
    </template>

    <template #render-cell-email="props">
      <a :href="`mailto:${props.row.email}`" class="text-link">
        {{ props.row.email }}
      </a>
    </template>

    <template #render-cell-isActive="props">
      <BooleanValue :only-true="true" :value="props.row.isActive" true-icon="check_circle" />
    </template>

    <template #render-cell-isStaff="props">
      <BooleanValue :only-true="true" :value="props.row.isStaff" true-icon="check_circle" />
    </template>
  </DataTable>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { BooleanValue, DataTable, DetailPopover, TagPill } from "@/components";
import { userListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { formatDate, getColumns, getDefaults, nully } from "@/utils";

import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "UserList",
  components: {
    BooleanValue,
    DetailPopover,
    DataTable,
    TagPill,
  },
  setup() {
    useMeta({ title: "Users" });
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No users found.";
    const title = "Users";

    const fetchData = async (query) => {
      const request = requests.users.getUsers(query);
      await fetchAPI(request);
      if (success.value)
        await userListSchema.validate(data.value.data, { stripUnknown: false }).then((value) => {
          columns.value = getColumns(columnMap);
          pagination.value.rowsNumber = data.value.count;
          rows.value = value;
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
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap));

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);

    return {
      columns,
      loading,
      filterList,
      formatDate,
      noData,
      nully,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      onRequest,
      pagination,
      rows,
      search,
      sortList,
      title,
      visibleColumns,
    };
  },
});
</script>
