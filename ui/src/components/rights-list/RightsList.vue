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
    resource="rights policies"
    grid
  >
    <template #grid-avatar="props">
      <q-icon
        :color="getStatusColours(props.row.rightsStatus.id).text"
        :name="getStatusIcon(props.row.rightsStatus.id)"
        size="22px"
      />
    </template>

    <template #grid-main="props">
      <DetailPopover
        :link-target="{ name: 'Rights Policy', params: { id: props.row.id } }"
        :link-text="props.row.name"
        link-class="text-h7 title-link"
      >
        <div class="text-detail text-weight-medium text-grey-8 q-mb-sm">
          Created on {{ formatDate(props.row.creationTimestamp, "DATETIME_AT") }} by
          {{ props.row.creationUser.username }}
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
        class="q-ml-sm"
        colour="orange-1"
        module="standalone"
        name="licence"
        size="xs"
        text-colour="orange-8"
      />
      <TagPill
        v-if="props.row.publicDisplay"
        :name="props.row.noticeDisplay ? 'display+notice' : 'display'"
        class="q-ml-sm"
        colour="light-blue-1"
        module="standalone"
        size="xs"
        text-colour="light-blue-8"
      />
    </template>

    <template #grid-detail="props">
      <div class="text-detail text-weight-medium text-grey-8">
        <span v-if="props.row.rights" v-text="props.row.rights" />
        <span v-else>No rights specified</span>
      </div>
    </template>

    <template #grid-counter="props">
      <q-icon
        v-if="props.row.commentCount"
        class="text-weight-bold q-mr-xs"
        name="chat_bubble_outline"
        size="17px"
      />
      <div v-if="props.row.commentCount" class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.commentCount }}
      </div>
    </template>

    <template #grid-counter-extra="props">
      <q-btn
        v-if="props.row.attachments"
        @click.stop="openURL(props.row.attachments.source)"
        color="blue-gray-6"
        icon="o_text_snippet"
        size="sm"
        target="_blank"
        text-color="blue-gray-6"
        dense
        flat
      />
    </template>

    <template #render-cell-name="props">
      <router-link :to="{ name: 'Rights', params: { id: props.row.id } }" class="text-link">
        {{ props.row.name }}
      </router-link>
    </template>

    <template #render-cell-rightsStatus="props">
      {{ props.row.rightsStatus.name }}
    </template>

    <template #render-cell-publicDisplay="props">
      <BooleanValue
        :only-true="true"
        :only-true-green="false"
        :value="!props.row.publicDisplay"
        true-icon="remove_circle"
      />
    </template>

    <template #render-cell-noticeDisplay="props">
      <BooleanValue :only-true="true" :value="props.row.noticeDisplay" true-icon="verified" />
    </template>

    <template #render-cell-attachments="props">
      <q-btn
        v-if="props.row.attachments"
        @click.stop="openURL(props.row.attachments.url)"
        color="blue-gray-6"
        icon="text_snippet"
        size="sm"
        target="_blank"
        text-color="blue-gray-6"
        flat
      />
    </template>
  </DataTable>
</template>

<script>
import { openURL } from "quasar";
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { BooleanValue, DataTable, DetailPopover, TagPill } from "@/components";
import { rightsListSchema } from "@/schemas";
import { useAPI, useConstants, usePagination, useStores } from "@/use";
import { formatDate, getColumns, getDefaults } from "@/utils";

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
