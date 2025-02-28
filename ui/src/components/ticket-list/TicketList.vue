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
    <template v-slot:grid-avatar="props">
      <q-icon
        :name="props.row.status ? 'check_circle_outline' : 'error_outline'"
        :color="props.row.status ? 'purple-8' : 'green-8'"
        size="22px"
      />
    </template>

    <template v-slot:grid-main="props">
      <DetailPopover
        linkClass="text-h7 title-link"
        :linkTarget="{ name: 'Ticket', params: { id: props.row.number } }"
        :linkText="props.row.subject"
      >
        <div class="text-detail text-weight-medium text-grey-8 q-mb-sm">
          {{ props.row.creationUser.username }}
          {{ formatDate(props.row.creationTimestamp, false) }}
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
        size="xs"
        module="ticket"
        class="q-ml-sm"
      />
    </template>

    <template v-slot:grid-detail="props">
      <div class="text-detail text-weight-medium text-grey-8">
        <span
          v-text="
            `#${props.row.number} opened ${formatDate(props.row.creationTimestamp, false)} by `
          "
        />
        <DetailPopover showAvatar :userData="props.row.creationUser" />
        <template v-if="props.row.status && props.row.closingUser">
          <span v-text="`, closed ${formatDate(props.row.closingDate, false)} by `" />
          <DetailPopover :userData="props.row.closingUser" />
        </template>
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
        v-if="props.row.file"
        flat
        dense
        @click.stop="openURL(props.row.file.source)"
        target="_blank"
        color="blue-gray-6"
        size="sm"
        icon="o_text_snippet"
        text-color="blue-gray-6"
      />
      <q-btn
        v-if="props.row.url"
        flat
        dense
        @click.stop="openURL(props.row.url)"
        target="_blank"
        color="blue-gray-6"
        size="sm"
        icon="link"
        text-color="blue-gray-6"
      />
    </template>

    <template v-slot:render-cell-tags="props">
      <TagPill
        v-for="(tag, idx) in cleanTags(props.row.tags)"
        :key="idx"
        :name="tag.tag"
        :type="tag.tag"
        module="ticket"
      />
    </template>

    <template v-slot:render-cell-status="props">
      <q-icon
        :name="props.row.status ? 'error_outline' : 'check_circle_outline'"
        :color="props.row.status ? 'green-8' : 'purple-8'"
        size="16px"
      />
    </template>

    <template v-slot:render-cell-subject="props">
      <router-link
        class="text-subtitle2 text-link"
        :to="{ name: 'Ticket', params: { id: props.row.number } }"
      >
        {{ props.row.subject }}
      </router-link>
    </template>

    <template v-slot:render-cell-file="props">
      <q-btn
        v-if="props.row.file"
        flat
        @click.stop="openURL(props.row.file.source)"
        target="_blank"
        color="blue-gray-6"
        size="sm"
        icon="o_text_snippet"
        text-color="blue-gray-6"
      />
    </template>

    <template v-slot:render-cell-commentCount="props">
      <q-icon
        name="chat_bubble_outline"
        size="17px"
        v-if="props.row.commentCount"
        class="text-weight-bold q-mr-xs"
      />
      <span v-if="props.row.commentCount" class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.commentCount }}
      </span>
    </template>

    <template v-slot:render-cell-creationUser="props">
      <DetailPopover showAvatar :userData="props.row.creationUser" />
    </template>
  </DataTable>
</template>

<script>
import { useMeta, openURL } from "quasar";
import { useRoute } from "vue-router";
import { filter as rFilter } from "ramda";
import { defineComponent, provide, ref } from "vue";
import { requests } from "@/api";
import { DataTable, DetailPopover, TagPill } from "@/components";
import { formatDate, getColumns, getDefaults } from "@/utils";
import { ticketListSchema } from "@/schemas";
import { useAPI, useConstants, useEditing, usePagination, useStores } from "@/use";
import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "TicketList",
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    DetailPopover,
    DataTable,
    TagPill,
  },
  setup(props, context) {
    if (!props.embedded) useMeta({ title: "Issue Tickets" });
    const $route = useRoute();
    const { auth } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const { ticketTagColours } = useConstants();
    const { postSubmitRefreshWatcher } = useEditing();
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
        ? requests.tickets.getUserTickets(auth.user.userId)
        : requests.tickets.getTickets(query);
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

    postSubmitRefreshWatcher(fetchData);

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
