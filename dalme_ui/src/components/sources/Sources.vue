<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
        :title="title"
        :rows="rows"
        :columns="columns"
        :no-data-label="noData"
        :filter="filter"
        :title-class="{ 'text-h6': true }"
        :loading="loading"
        @request="onRequest"
        v-model:pagination="pagination"
        row-key="id"
      >
        <template v-slot:top-right>
          <q-input
            borderless
            dense
            debounce="300"
            v-model="filter"
            placeholder="Search"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>

        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <router-link
              class="text-subtitle2"
              :to="{ name: 'Source', params: { id: props.row.id } }"
            >
              {{ props.value }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-primaryDataset="props">
          <q-td :props="props">
            <router-link :to="{ name: 'Set', params: { id: props.value.id } }">
              {{ props.value.name }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-noRecords="props">
          <q-td :props="props">
            {{ props.value }}
          </q-td>
        </template>

        <template v-slot:body-cell-defaultRights="props">
          <q-td :props="props">
            <router-link
              v-if="props.row.attributes.defaultRights"
              :to="{
                name: 'Rights',
                params: {
                  id: props.row.attributes.defaultRights.id.id,
                },
              }"
            >
              {{ props.row.attributes.defaultRights.name }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-archiveUrl="props">
          <q-td :props="props">
            <a
              v-if="props.row.attributes.archiveUrl"
              :href="props.row.attributes.archiveUrl"
              target="_blank"
            >
              Visit Website
            </a>
          </q-td>
        </template>

        <template v-slot:body-cell-owner="props">
          <q-td :props="props">
            <router-link
              :to="{
                name: 'User',
                params: { username: props.value.username },
              }"
            >
              {{ props.value.fullName }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-locale="props">
          <q-td :props="props">
            {{ getLocale(props.row.attributes.locale) }}
          </q-td>
        </template>

        <template v-slot:body-cell-recordType="props">
          <q-td :props="props">
            {{ props.row.attributes.recordType }}
          </q-td>
        </template>

        <template v-slot:body-cell-date="props">
          <q-td :props="props">
            <span v-html="renderDate(props.row.attributes)"></span>
          </q-td>
        </template>

        <template v-slot:body-cell-language="props">
          <q-td :props="props">
            {{ props.row.attributes.language[0].name }}
          </q-td>
        </template>

        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-badge outline color="primary">
              {{ props.row.workflow.status.text }}
            </q-badge>
          </q-td>
        </template>

        <template v-slot:body-cell-helpFlag="props">
          <q-td :props="props">
            <q-icon
              v-if="props.row.workflow.helpFlag"
              name="error"
              class="text-red"
              size="sm"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-activity="props">
          <q-td :props="props">
            <span>
              <router-link
                :to="{
                  name: 'User',
                  params: { username: props.row.workflow.activity.username },
                }"
              >
                {{ props.row.workflow.activity.user }}
              </router-link>
              <br />
              {{ props.row.workflow.activity.timestamp }}
            </span>
          </q-td>
        </template>

        <template v-slot:body-cell-isPrivate="props">
          <q-td :props="props">
            <q-icon :name="props.row.isPrivate ? 'done' : 'close'" />
          </q-td>
        </template>

        <template v-slot:body-cell-isPublic="props">
          <q-td :props="props">
            <q-icon :name="props.row.isPublic ? 'done' : 'close'" />
          </q-td>
        </template>

        <template v-slot:body-cell-authority="props">
          <q-td :props="props">
            {{ props.row.attributes.authority }}
          </q-td>
        </template>

        <template v-slot:body-cell-format="props">
          <q-td :props="props">
            {{ props.row.attributes.format }}
          </q-td>
        </template>

        <template v-slot:body-cell-support="props">
          <q-td :props="props">
            {{ props.row.attributes.support }}
          </q-td>
        </template>

        <template v-slot:body-cell-zoteroKey="props">
          <q-td :props="props">
            {{ props.row.attributes.zoteroKey }}
          </q-td>
        </template>
      </q-table>
      <OpaqueSpinner :showing="loading" />
    </q-card>
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { keys, map } from "ramda";
import { defineComponent, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
import { sourceListSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";

import { columnsByType } from "./columns";

export default defineComponent({
  name: "Sources",
  components: {
    OpaqueSpinner,
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

    const noData = "No sources found.";
    const getColumns = () => {
      const columnMap = columnsByType(sourceType.value);
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys(columnMap));
    };

    const renderDate = (attributes) => {
      if (attributes.startDate && attributes.endDate) {
        return `${attributes.startDate.name}<br>${attributes.endDate.name}`;
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
            columns.value = getColumns();
            pagination.value.rowsNumber = value.recordsTotal;
            rows.value.splice(0, rows.value.length, ...value.data);
            loading.value = false;
          });
    };

    const {
      fetchDataPaginated,
      filter,
      pagination,
      onRequest,
      resetPagination,
    } = usePagination(fetchData);

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
      filter,
      getLocale,
      loading,
      noData,
      onRequest,
      pagination,
      renderDate,
      rows,
      title,
    };
  },
});
</script>
