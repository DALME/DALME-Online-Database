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
    <template #grid-avatar="props">
      <q-icon
        :color="props.row.status ? 'purple-8' : 'green-8'"
        :name="props.row.status ? 'check_circle_outline' : 'error_outline'"
        size="22px"
      />
    </template>

    <template #grid-main="props">
      <DetailPopover
        :link-target="{ name: 'Ticket', params: { id: props.row.number } }"
        :link-text="props.row.subject"
        link-class="text-h7 title-link"
      >
        <div class="text-detail text-weight-medium text-grey-8 q-mb-sm">
          {{ props.row.creationUser.username }}
          {{ formatDate(props.row.creationTimestamp, "DATETIME_AT") }}
        </div>
        <div class="text-h8 q-mb-xs">
          <span class="text-grey-7">#{{ props.row.number }}</span>
          {{ props.row.subject }}
        </div>
        <div class="text-detail ellipsis-3-lines">
          {{ props.row.description }}
        </div>
      </DetailPopover>
      <TagPill
        v-for="(tag, idx) in cleanTags(props.row.tags)"
        :key="idx"
        :name="tag.tag"
        :type="tag.tag"
        class="q-ml-sm"
        module="ticket"
        size="xs"
      />
    </template>

    <template #grid-detail="props">
      <div class="text-detail text-weight-medium text-grey-8">
        <span
          v-text="
            `#${props.row.number} opened on ${formatDate(
              props.row.creationTimestamp,
              'DATETIME_AT',
            )} by `
          "
        />
        <DetailPopover :user-data="props.row.creationUser" show-avatar />
        <template v-if="props.row.status && props.row.closingUser">
          <span v-text="`, closed on ${formatDate(props.row.closingDate, 'DATETIME_AT')} by `" />
          <DetailPopover :user-data="props.row.closingUser" />
        </template>
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
        v-if="props.row.file"
        @click.stop="openURL(props.row.file.source)"
        color="blue-gray-6"
        icon="o_text_snippet"
        size="sm"
        target="_blank"
        text-color="blue-gray-6"
        dense
        flat
      />
      <q-btn
        v-if="props.row.url"
        @click.stop="openURL(props.row.url)"
        color="blue-gray-6"
        icon="link"
        size="sm"
        target="_blank"
        text-color="blue-gray-6"
        dense
        flat
      />
    </template>

    <template #render-cell-tags="props">
      <TagPill
        v-for="(tag, idx) in cleanTags(props.row.tags)"
        :key="idx"
        :name="tag.tag"
        :type="tag.tag"
        module="ticket"
      />
    </template>

    <template #render-cell-status="props">
      <q-icon
        :color="props.row.status ? 'green-8' : 'purple-8'"
        :name="props.row.status ? 'error_outline' : 'check_circle_outline'"
        size="16px"
      />
    </template>

    <template #render-cell-subject="props">
      <router-link
        :to="{ name: 'Ticket', params: { id: props.row.number } }"
        class="text-subtitle2 text-link"
      >
        {{ props.row.subject }}
      </router-link>
    </template>

    <template #render-cell-file="props">
      <q-btn
        v-if="props.row.file"
        @click.stop="openURL(props.row.file.source)"
        color="blue-gray-6"
        icon="o_text_snippet"
        size="sm"
        target="_blank"
        text-color="blue-gray-6"
        flat
      />
    </template>

    <template #render-cell-commentCount="props">
      <q-icon
        v-if="props.row.commentCount"
        class="text-weight-bold q-mr-xs"
        name="chat_bubble_outline"
        size="17px"
      />
      <span v-if="props.row.commentCount" class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.commentCount }}
      </span>
    </template>

    <template #render-cell-creationUser="props">
      <DetailPopover :user-data="props.row.creationUser" show-avatar />
    </template>
  </DataTable>
</template>

<script>
import { openURL, useMeta } from "quasar";
import { filter as rFilter } from "ramda";
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { DataTable, DetailPopover, TagPill } from "@/components";
import { ticketListSchema } from "@/schemas";
import { useAPI, useConstants, usePagination, useStores } from "@/use";
import { formatDate, getColumns, getDefaults } from "@/utils";

import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "TicketList",
  components: {
    DetailPopover,
    DataTable,
    TagPill,
  },
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, context) {
    if (!props.embedded) useMeta({ title: "Issue Tickets" });
    const $route = useRoute();
    const { auth } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const { ticketTagColours } = useConstants();
    const columns = ref([]);
    const rows = ref([]);
    const noData = props.embedded ? "No tickets created" : "No tickets found";
    const title = props.embedded ? "My Tickets" : "Tickets";
    const tagsFilter = ref([]);

    const cleanTags = (tags) => {
      return rFilter((tag) => tag.tag, tags);
    };

    const fetchData = async (query) => {
      const request = props.embedded
        ? requests.tickets.getByUser(auth.user.id)
        : requests.tickets.list(query);
      await fetchAPI(request);
      if (success.value)
        await ticketListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
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
    } = usePagination(fetchData, $route.name, getDefaults(columnMap), props.embedded);

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);

    return {
      context,
      cleanTags,
      columns,
      filterList: filterList(auth.user.userId),
      formatDate,
      loading,
      noData,
      openURL,
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
      tagsFilter,
      ticketTagColours,
      tagList: Object.keys(ticketTagColours),
      title,
      visibleColumns,
    };
  },
});
</script>
