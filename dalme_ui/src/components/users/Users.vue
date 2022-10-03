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
      <BooleanIcon
        :value="props.row.isActive"
        :onlyTrue="true"
        trueIcon="check_circle"
      />
    </template>

    <template v-slot:render-cell-isStaff="props">
      <BooleanIcon
        :value="props.row.isStaff"
        :onlyTrue="true"
        trueIcon="check_circle"
      />
    </template>
  </BasicTable>
</template>

<script>
import { defineComponent, onMounted, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import BasicTable from "@/components/basic-table/BasicTable.vue";
import { BooleanIcon, getColumns, getDefaults } from "@/components/utils";
import { userListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { columnMap } from "./columns";

export default defineComponent({
  name: "Users",
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
    const noData = "No users found.";
    const title = "Users";

    const fetchData = async () => {
      const request = requests.users.getUsers();
      await fetchAPI(request);
      if (success.value)
        await userListSchema
          .validate(data.value.data, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns(columnMap);
            pagination.value.rowsNumber = data.value.recordsFiltered;
            pagination.value.rowsTotal = data.value.recordsTotal;
            rows.value = value;
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
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap));

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);

    onMounted(async () => await fetchData());

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
