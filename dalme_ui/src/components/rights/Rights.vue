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
        class="text-link"
        :to="{ name: 'Rights', params: { id: props.row.id } }"
      >
        {{ props.row.name }}
      </router-link>
    </template>

    <template v-slot:render-cell-rightsStatus="props">
      {{ props.row.rightsStatus.name }}
    </template>

    <template v-slot:render-cell-publicDisplay="props">
      <BooleanIcon
        :value="!props.row.publicDisplay"
        :onlyTrue="true"
        :onlyTrueGreen="false"
        trueIcon="remove_circle"
      />
    </template>

    <template v-slot:render-cell-noticeDisplay="props">
      <BooleanIcon
        :value="props.row.noticeDisplay"
        :onlyTrue="true"
        trueIcon="verified"
      />
    </template>

    <template v-slot:render-cell-attachments="props">
      <q-btn
        v-if="props.row.attachments"
        flat
        @click.stop="openURL(props.row.attachments.url)"
        target="_blank"
        color="blue-gray-6"
        size="sm"
        icon="text_snippet"
        text-color="blue-gray-6"
      />
    </template>
  </BasicTable>
</template>

<script>
import { openURL } from "quasar";
import { defineComponent, onMounted, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import BasicTable from "@/components/basic-table/BasicTable.vue";
import { BooleanIcon, getColumns, getDefaults } from "@/components/utils";
import { rightsListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { columnMap } from "./columns";

export default defineComponent({
  name: "Rights",
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
    const noData = "No rights found.";
    const title = "Rights";

    const fetchData = async () => {
      const request = requests.rights.getRights();
      await fetchAPI(request);
      if (success.value)
        await rightsListSchema
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
      openURL,
      onRequest,
      pagination,
      rows,
      title,
      visibleColumns,
    };
  },
});
</script>
