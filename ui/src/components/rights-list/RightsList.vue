<template>
  <DataTable
    grid
    :columns="columns"
    :search="search"
    :filterList="filterList"
    :loading="loading"
    :noData="noData"
    resource="rights policies"
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
      <q-icon
        :name="getStatusIcon(props.row.rightsStatus.id)"
        :color="getStatusColours(props.row.rightsStatus.id).text"
        size="22px"
      />
    </template>

    <template v-slot:grid-main="props">
      <DetailPopover
        linkClass="text-h7 title-link"
        :linkTarget="{ name: 'Rights Policy', params: { id: props.row.id } }"
        :linkText="props.row.name"
      >
        <div class="text-detail text-weight-medium text-grey-8 q-mb-sm">
          Created by {{ props.row.creationUser.username }}
          {{ formatDate(props.row.creationTimestamp, false) }}
        </div>
        <div v-if="props.row.rightsHolder" class="text-h8 q-mb-xs">
          <span class="text-grey-7">Rights Holder:</span>
          {{ props.row.rightsHolder }}
        </div>
        <div v-if="props.row.rights" class="text-detail q-mb-xs">
          {{ props.row.rights }}
        </div>
        <div v-if="props.row.licence" class="text-detail q-mb-xs">
          <b>Licence:</b> {{ props.row.licence }}
        </div>
        <div v-if="props.row.rightsNotice" class="text-detail q-mb-xs">
          <b>Notice:</b> {{ props.row.rightsNotice }}
        </div>
      </DetailPopover>
      <TagPill
        v-if="props.row.licence"
        name="licence"
        colour="orange-1"
        textColour="orange-8"
        size="xs"
        module="standalone"
        class="q-ml-sm"
      />
      <TagPill
        v-if="props.row.publicDisplay"
        :name="props.row.noticeDisplay ? 'display+notice' : 'display'"
        colour="light-blue-1"
        textColour="light-blue-8"
        size="xs"
        module="standalone"
        class="q-ml-sm"
      />
    </template>

    <template v-slot:grid-detail="props">
      <div class="text-detail text-weight-medium text-grey-8">
        <span v-if="props.row.rights" v-text="props.row.rights" />
        <span v-else>No rights specified</span>
      </div>
    </template>

    <template v-slot:grid-counter="props">
      <q-icon
        name="chat_bubble_outline"
        size="17px"
        v-if="props.row.commentCount"
        class="text-weight-bold q-mr-xs"
      />
      <div v-if="props.row.commentCount" class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.commentCount }}
      </div>
    </template>

    <template v-slot:grid-counter-extra="props">
      <q-btn
        v-if="props.row.attachments"
        flat
        dense
        @click.stop="openURL(props.row.attachments.source)"
        target="_blank"
        color="blue-gray-6"
        size="sm"
        icon="o_text_snippet"
        text-color="blue-gray-6"
      />
    </template>

    <template v-slot:render-cell-name="props">
      <router-link class="text-link" :to="{ name: 'Rights', params: { id: props.row.id } }">
        {{ props.row.name }}
      </router-link>
    </template>

    <template v-slot:render-cell-rightsStatus="props">
      {{ props.row.rightsStatus.name }}
    </template>

    <template v-slot:render-cell-publicDisplay="props">
      <BooleanValue
        :value="!props.row.publicDisplay"
        :onlyTrue="true"
        :onlyTrueGreen="false"
        trueIcon="remove_circle"
      />
    </template>

    <template v-slot:render-cell-noticeDisplay="props">
      <BooleanValue :value="props.row.noticeDisplay" :onlyTrue="true" trueIcon="verified" />
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
  </DataTable>
</template>

<script>
import { openURL } from "quasar";
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { BooleanValue, DetailPopover, TagPill, DataTable } from "@/components";
import { formatDate, getColumns, getDefaults } from "@/utils";
import { rightsListSchema } from "@/schemas";
import { useAPI, useConstants, usePagination, useStores } from "@/use";
import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "RightsList",
  components: {
    DetailPopover,
    BooleanValue,
    DataTable,
    TagPill,
  },
  setup() {
    const $route = useRoute();
    const { auth } = useStores();
    const { rightsIconById, rightsColoursById } = useConstants();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const noData = "No rights found.";
    const title = "Rights";

    const getStatusIcon = (id) => rightsIconById[id];
    const getStatusColours = (id) => rightsColoursById[id];

    const fetchData = async (query) => {
      const request = requests.rights.getRights(query);
      await fetchAPI(request);
      if (success.value)
        await rightsListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
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
      filterList: filterList(auth.user.userId),
      formatDate,
      getStatusIcon,
      getStatusColours,
      loading,
      noData,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      openURL,
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
