<template>
  <Table
    grid
    useExpansion
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
      <Tag
        mini
        module="workflow"
        size="22px"
        :type="props.row.workflow.status.tag"
        :wfStage="props.row.workflow.stage"
        :wfStatus="props.row.workflow.wfStatus"
      />
    </template>

    <template v-slot:grid-main="props">
      <DetailPopover
        linkClass="text-h7 title-link"
        :linkTarget="{ name: 'Source', params: { id: props.row.id } }"
        :linkText="props.row.name"
      >
        <div class="text-h8 q-mb-xs">
          {{ props.row.name }}
        </div>
      </DetailPopover>
      <Tag
        v-if="props.row.workflow.isPublic"
        name="public"
        colour="light-blue-1"
        textColour="light-blue-9"
        size="xs"
        module="standalone"
        class="q-ml-sm"
      />
      <Tag
        v-if="props.row.isPrivate"
        name="private"
        colour="deep-orange-1"
        textColour="deep-orange-8"
        size="xs"
        module="standalone"
        class="q-ml-sm"
      />
    </template>

    <template v-slot:grid-detail="props">
      <span class="text-detail text-weight-medium text-grey-8">
        {{ props.row.attributes.recordType }} |
        <span v-html="renderDate(props.row.attributes)"></span>
      </span>
    </template>

    <template v-slot:grid-counter="props">
      <q-icon
        name="o_import_contacts"
        size="17px"
        v-if="props.row.noFolios"
        class="text-weight-bold q-mr-xs"
      />
      <div class="text-grey-8 text-weight-bold text-detail">
        {{ props.row.noFolios }}
      </div>
    </template>

    <template v-slot:grid-counter-extra="props">
      <q-icon
        name="flag"
        size="17px"
        v-if="props.row.workflow.helpFlag"
        color="red-4"
        class="text-weight-bold q-mr-xs"
      />
    </template>

    <template v-slot:render-cell-name="props">
      <router-link
        class="text-subtitle2 text-link"
        :to="{ name: 'Source', params: { id: props.row.id } }"
      >
        {{ props.row.name }}
      </router-link>
    </template>

    <template v-slot:render-cell-primaryDataset="props">
      <router-link
        class="text-link"
        :to="{ name: 'Set', params: { id: props.row.primaryDataset.id } }"
      >
        {{ props.row.primaryDataset.name }}
      </router-link>
    </template>

    <template v-slot:render-cell-noRecords="props">
      {{ props.row.noRecords }}
    </template>

    <template v-slot:render-cell-defaultRights="props">
      <router-link
        v-if="props.row.attributes.defaultRights"
        class="text-link"
        :to="{
          name: 'Rights',
          params: {
            id: props.row.attributes.defaultRights.id.id,
          },
        }"
      >
        {{ props.row.attributes.defaultRights.name }}
      </router-link>
    </template>

    <template v-slot:render-cell-url="props">
      <a
        v-if="props.row.attributes.url"
        :href="props.row.attributes.url"
        class="text-link"
        target="_blank"
      >
        Visit Website
      </a>
    </template>

    <template v-slot:render-cell-owner="props">
      <router-link
        class="text-link"
        :to="{
          name: 'User',
          params: { username: props.row.owner.username },
        }"
      >
        {{ props.row.owner.fullName }}
      </router-link>
    </template>

    <template v-slot:render-cell-locale="props">
      {{ getLocale(props.row.attributes.locale) }}
    </template>

    <template v-slot:render-cell-recordType="props">
      {{ props.row.attributes.recordType }}
    </template>

    <template v-slot:render-cell-date="props">
      <span v-html="renderDate(props.row.attributes)"></span>
    </template>

    <template v-slot:render-cell-language="props">
      {{ props.row.attributes.language[0].name }}
    </template>

    <template v-slot:render-cell-status="props">
      <Tag
        :name="props.row.workflow.status.text"
        :type="props.row.workflow.status.tag"
        module="workflow"
      />
    </template>

    <template v-slot:render-cell-helpFlag="props">
      <q-icon
        v-if="props.row.workflow.helpFlag"
        name="flag"
        class="text-red"
        size="xs"
      />
    </template>

    <template v-slot:render-cell-activity="props">
      <span>
        <router-link
          class="text-link"
          :to="{
            name: 'User',
            params: { username: props.row.workflow.lastUser.username },
          }"
        >
          {{ props.row.workflow.lastUser.profile.fullName }}
        </router-link>
        <br />
        {{ props.row.workflow.lastModified }}
      </span>
    </template>

    <template v-slot:render-cell-isPrivate="props">
      <BooleanIcon
        :value="props.row.isPrivate"
        :onlyTrue="true"
        :onlyTrueGreen="false"
        trueIcon="lock"
      />
    </template>

    <template v-slot:render-cell-isPublic="props">
      <BooleanIcon
        :value="props.row.workflow.isPublic"
        :onlyTrue="true"
        trueIcon="public"
      />
    </template>

    <template v-slot:render-cell-authority="props">
      {{ props.row.attributes.authority }}
    </template>

    <template v-slot:render-cell-format="props">
      {{ props.row.attributes.format }}
    </template>

    <template v-slot:render-cell-support="props">
      {{ props.row.attributes.support }}
    </template>

    <template v-slot:render-cell-zoteroKey="props">
      {{ props.row.attributes.zoteroKey }}
    </template>
  </Table>
</template>

<script>
import { useMeta } from "quasar";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { requests } from "@/api";
import { Table } from "@/components";
import {
  BooleanIcon,
  DetailPopover,
  getColumns,
  getDefaults,
  Tag,
} from "@/components/utils";
import { sourceListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";
import { columnsByType } from "./columns";
import { filtersByType, sortByType } from "./filters";

export default defineComponent({
  name: "Sources",
  components: {
    BooleanIcon,
    DetailPopover,
    Table,
    Tag,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const sourceType = ref("");
    const sourceTypeAPI = ref("");
    const title = ref("");

    useMeta(() => ({ title: title.value }));

    const columnMap = computed(() => {
      return columnsByType($route.meta.sourceType);
    });

    const filterList = computed(() => {
      return filtersByType($route.meta.sourceType);
    });

    const sortList = computed(() => {
      return sortByType($route.meta.sourceType);
    });

    const noData = "No sources found.";
    const renderDate = (attributes) => {
      if (attributes.startDate && attributes.endDate) {
        return `${attributes.startDate.name} – ${attributes.endDate.name}`;
      }
      if (attributes.startDate) {
        return attributes.startDate.name;
      }
      return attributes.date.name;
    };

    const getLocale = (data) => {
      return !data ? "" : Array.isArray(data) ? data[0].name : data.name;
    };

    const fetchData = async (query) => {
      const request = requests.sources.getSources(sourceTypeAPI.value, query);
      const schema = sourceListSchema(sourceType.value);
      await fetchAPI(request);
      if (success.value)
        await schema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns(columnMap.value);
            pagination.value.rowsNumber = value.recordsFiltered;
            pagination.value.rowsTotal = value.recordsTotal;
            rows.value.splice(0, rows.value.length, ...value.data);
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
      resetPagination,
      visibleColumns,
    } = usePagination(fetchData, $route.name, getDefaults(columnMap.value));

    provide("pagination", { pagination, fetchDataPaginated });
    provide("columns", columns);
    provide("visibleColumns", visibleColumns);
    provide("activeFilters", activeFilters);

    onBeforeRouteLeave(() => {
      if (loading.value) return false;
    });

    watch(
      () => $route.name,
      async (to) => {
        const reload = [
          "Archives",
          "Archival Files",
          "Records",
          "Bibliography",
        ];
        const reloadPage = async () => {
          loading.value = true;
          sourceTypeAPI.value = $route.meta.sourceTypeAPI;
          sourceType.value = $route.meta.sourceType;
          const setTitle = () => (title.value = to);
          let updateTitle = true;
          if (!title.value) {
            setTitle();
            updateTitle = false;
          }
          resetPagination();
          await fetchDataPaginated();
          if (updateTitle) setTitle();
        };
        if (reload.includes(to)) {
          await reloadPage();
        }
      },
      { immediate: true },
    );

    return {
      columns,
      getLocale,
      filterList,
      loading,
      noData,
      onChangeSearch,
      onChangePage,
      onChangeRowsPerPage,
      onChangeFilters,
      onClearFilters,
      onRequest,
      pagination,
      renderDate,
      rows,
      search,
      sortList,
      title,
      visibleColumns,
    };
  },
});
</script>
