<template>
  <DataTable
    grid
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
    <template v-slot:grid-avatar="props">
      <q-avatar v-if="notNully(props.row.avatar)" size="24px">
        <img :src="props.row.avatar" />
      </q-avatar>
      <q-icon v-else name="account_circle" size="sm" />
    </template>

    <template v-slot:grid-main="props">
      <DetailPopover
        linkClass="text-h7 title-link"
        :linkTarget="{ name: 'User', params: { username: props.row.username } }"
        :linkText="props.row.fullName"
      >
        <div class="text-h8 q-mb-xs">
          {{ props.row.username }}
        </div>
      </DetailPopover>
      <TagWidget
        v-if="props.row.isActive"
        name="active"
        colour="light-green-1"
        textColour="light-green-9"
        size="xs"
        module="standalone"
        class="q-ml-sm"
      />
      <TagWidget
        v-if="props.row.isStaff"
        name="staff"
        colour="light-blue-1"
        textColour="light-blue-8"
        size="xs"
        module="standalone"
        class="q-ml-sm"
      />
      <TagWidget
        v-if="props.row.isSuperuser"
        name="super"
        colour="orange-1"
        textColour="orange-8"
        size="xs"
        module="standalone"
        class="q-ml-sm"
      />
    </template>

    <template v-slot:grid-detail="props">
      <span class="text-detail text-weight-medium text-grey-8">
        #{{ props.row.id }} | {{ props.row.username }} |
        <a class="text-link" :href="`mailto:${props.row.email}`">
          {{ props.row.email }}
        </a>
      </span>
    </template>

    <template v-slot:grid-counter="props">
      <div class="text-detail text-weight-medium text-grey-8 q-ml-auto">
        Joined {{ formatDate(props.row.dateJoined, false) }}
      </div>
    </template>

    <template v-slot:grid-counter-extra="props">
      <div class="text-detail text-weight-medium text-grey-8 q-ml-auto">
        Last active
        {{ formatDate(props.row.lastLogin, false) }}
      </div>
    </template>

    <template v-slot:render-cell-username="props">
      <router-link
        class="text-link"
        :to="{ name: 'User', params: { username: props.row.username } }"
      >
        {{ props.row.username }}
      </router-link>
    </template>

    <template v-slot:render-cell-id="props">
      {{ props.row.id }}
    </template>

    <template v-slot:render-cell-email="props">
      <a class="text-link" :href="`mailto:${props.row.email}`">
        {{ props.row.email }}
      </a>
    </template>

    <template v-slot:render-cell-isActive="props">
      <BooleanWidget :value="props.row.isActive" :onlyTrue="true" trueIcon="check_circle" />
    </template>

    <template v-slot:render-cell-isStaff="props">
      <BooleanWidget :value="props.row.isStaff" :onlyTrue="true" trueIcon="check_circle" />
    </template>
  </DataTable>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { formatDate, getColumns, getDefaults, notNully } from "@/utils";
import { BooleanWidget, DataTable, DetailPopover, TagWidget } from "@/components";
import { userListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "UserList",
  components: {
    BooleanWidget,
    DetailPopover,
    DataTable,
    TagWidget,
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
        await userListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
          columns.value = getColumns(columnMap);
          pagination.value.rowsNumber = data.value.filtered;
          pagination.value.rowsTotal = data.value.count;
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
      notNully,
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
