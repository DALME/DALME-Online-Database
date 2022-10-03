<template>
  <Table
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
    <template v-slot:toolbar-filtersets>
      <q-btn-dropdown
        flat
        dense
        label="Tags"
        no-caps
        menu-anchor="bottom right"
        menu-self="top right"
        content-class="menu-shadow"
      >
        <q-list bordered separator class="text-grey-9">
          <q-item dense class="q-pr-sm">
            <q-item-section class="text-weight-bold">
              Filter by Tag
            </q-item-section>
            <q-item-section avatar>
              <q-btn
                flat
                dense
                size="xs"
                color="grey-6"
                icon="close"
                @click="context.emit('clearFilters')"
              />
            </q-item-section>
          </q-item>
          <template v-for="(tag, idx) in tagList" :key="idx">
            <q-item
              clickable
              v-close-popup
              dense
              :class="
                tagsFilter.includes(tag)
                  ? 'text-weight-bold bg-indigo-1 text-indigo-5'
                  : 'text-grey-8'
              "
              @click="onChangeFilterTags(tag)"
            >
              <q-item-section side>
                <q-icon
                  name="circle"
                  :color="ticketTagColours[tag]['text']"
                  size="xs"
                />
              </q-item-section>
              <q-item-section>
                {{ tag }}
              </q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-btn-dropdown>
      <Chooser
        showHeader
        toggleIcon
        showSelectedItem
        label="Author"
        headerText="Filter by Author"
        target="users"
        @itemChosen="setAuthor"
        :clearFilters="onClearFilters"
      />
      <Chooser
        showHeader
        toggleIcon
        showSelectedItem
        label="Assignee"
        headerText="Filter by Assignee"
        target="users"
        @itemChosen="setAssignee"
        :clearFilters="onClearFilters"
      />
    </template>

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
        :linkTarget="{ name: 'Ticket', params: { id: props.row.id } }"
        :linkText="props.row.subject"
      >
        <div class="text-detail text-weight-medium text-grey-8 q-mb-sm">
          {{ props.row.creationUser.username }}
          {{ formatDate(props.row.creationTimestamp, false) }}
        </div>
        <div class="text-h8 q-mb-xs">
          <span class="text-grey-7">#{{ props.row.id }}</span>
          {{ props.row.subject }}
        </div>
        <div class="text-detail ellipsis-3-lines">
          {{ props.row.description }}
        </div>
      </DetailPopover>
      <Tag
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
            `#${props.row.id} opened ${formatDate(
              props.row.creationTimestamp,
              false,
            )} by `
          "
        />
        <DetailPopover showAvatar :userData="props.row.creationUser" />
        <template v-if="props.row.status && props.row.closingUser">
          <span
            v-text="`, closed ${formatDate(props.row.closingDate, false)} by `"
          />
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
      <div
        v-if="props.row.commentCount"
        class="text-grey-8 text-weight-bold text-detail"
      >
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
      <Tag
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
        :to="{ name: 'Ticket', params: { id: props.row.id } }"
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
      <span
        v-if="props.row.commentCount"
        class="text-grey-8 text-weight-bold text-detail"
      >
        {{ props.row.commentCount }}
      </span>
    </template>

    <template v-slot:render-cell-creationUser="props">
      <DetailPopover showAvatar :userData="props.row.creationUser" />
    </template>
  </Table>
</template>

<script>
import { openURL } from "quasar";
import { useRoute } from "vue-router";
import { filter as rFilter } from "ramda";
import { defineComponent, provide, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useConstantStore } from "@/stores/constants";
import { requests } from "@/api";
import { Table } from "@/components";
import {
  Chooser,
  DetailPopover,
  formatDate,
  getColumns,
  getDefaults,
  Tag,
} from "@/components/utils";
import { ticketListSchema } from "@/schemas";
import { useAPI, useEditing, usePagination } from "@/use";
import { columnMap } from "./columns";
import { filterList, sortList } from "./filters";

export default defineComponent({
  name: "Tickets",
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    Chooser,
    DetailPopover,
    Table,
    Tag,
  },
  setup(props, context) {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const $authStore = useAuthStore();
    const $constantStore = useConstantStore();
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
        ? requests.tickets.getUserTickets($authStore.userId)
        : requests.tickets.getTickets(query);
      await fetchAPI(request);
      if (success.value)
        await ticketListSchema
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
    } = usePagination(
      fetchData,
      $route.name,
      getDefaults(columnMap),
      props.embedded,
    );

    const setAuthor = (value) => {
      onChangeFilters({
        field: "creation_user",
        value: value,
      });
    };

    const setAssignee = (value) => {
      onChangeFilters({
        field: "assigned_to",
        value: value,
      });
    };

    const onChangeFilterTags = (value) => {
      let targetValue = "";
      if ("tags" in activeFilters.value) {
        let tags = activeFilters.value["tags"].split(",");
        if (tags.includes(value)) {
          tags = tags.slice(tags.indexOf(value), 1);
        } else {
          tags.push(value);
        }
        tagsFilter.value = tags;
        targetValue = tags.join(",");
      } else {
        tagsFilter.value.push(value);
        targetValue = value;
      }
      onChangeFilters({
        field: "tags",
        value: targetValue,
      });
    };

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);

    postSubmitRefreshWatcher(fetchData);

    return {
      context,
      cleanTags,
      columns,
      filterList,
      formatDate,
      loading,
      noData,
      openURL,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      onChangeFilterTags,
      onRequest,
      pagination,
      rows,
      setAuthor,
      setAssignee,
      search,
      sortList,
      tagsFilter,
      ticketTagColours: $constantStore.ticketTagColours,
      tagList: Object.keys($constantStore.ticketTagColours),
      title,
      visibleColumns,
    };
  },
});
</script>
