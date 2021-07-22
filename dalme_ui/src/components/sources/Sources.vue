<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <Spinner v-if="loading" />
      <q-table
        v-else
        :title="title"
        :rows="rows"
        :columns="columns"
        :visible-columns="visibleColumns"
        :no-data-label="noData"
        :filter="filter"
        :pagination="pagination"
        :title-class="{ 'text-h6': true }"
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
              :to="{ name: 'Source', params: { objId: props.row.id } }"
            >
              {{ props.value }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-primaryDataset="props">
          <q-td :props="props">
            <router-link
              :to="{ name: 'Set', params: { objId: props.value.objId } }"
            >
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
                  objId: props.row.attributes.defaultRights.id.objId,
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
            <router-link
              v-if="props.row.attributes.locale"
              :to="{
                name: 'Locale',
                params: {
                  objId: getLocaleData(props.row.attributes.locale).id.objId,
                },
              }"
            >
              {{ getLocaleData(props.row.attributes.locale).name }}
            </router-link>
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
            <router-link
              v-if="props.row.attributes.language[0]"
              :to="{
                name: 'Language',
                params: { objId: props.row.attributes.language[0].id.objId },
              }"
            >
              {{ props.row.attributes.language[0].name }}
            </router-link>
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
            <q-icon v-if="props.row.isPrivate" name="vpn_lock" size="xs" />
            <q-icon v-else name="public" size="xs" />
          </q-td>
        </template>

        <template v-slot:body-cell-isPublic="props">
          <q-td :props="props">
            <q-icon
              v-if="props.row.workflow.isPublic"
              name="public"
              size="xs"
            />
            <q-icon v-else name="vpn_lock" size="xs" />
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
    </q-card>
  </div>
</template>

<script>
import { isEmpty, keys, map, filter as rFilter } from "ramda";
import { useMeta } from "quasar";
import S from "string";
import { defineComponent, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { Spinner } from "@/components/utils";
import { sourceListSchema } from "@/schemas";
import { useAPI } from "@/use";

import { columnsByKind } from "./columns";

export default defineComponent({
  name: "Sources",
  components: {
    Spinner,
  },
  async setup() {
    const $route = useRoute();
    const { loading, success, data, fetchAPI } = useAPI();

    const columns = ref([]);
    const visibleColumns = ref([]);
    const rows = ref([]);
    const filter = ref("");
    const kind = ref("");
    const kindAPI = ref("");
    const title = ref("");

    useMeta(() => ({ title: title.value }));

    const noData = "No sources found.";
    const pagination = { rowsPerPage: 20 };

    const getColumns = (keys) => {
      const columnMap = columnsByKind(kind.value);
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys);
    };

    const fetchData = async () => {
      const request = requests.sources.getSources(kindAPI.value);
      const schema = sourceListSchema(kind.value);
      await fetchAPI(request);
      if (success.value)
        await schema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            if (!isEmpty(value)) {
              columns.value = getColumns(keys(columnsByKind(kind.value)));
              visibleColumns.value = map(
                (column) => column.field,
                rFilter(
                  (column) => !["id"].includes(column.field),
                  columns.value,
                ),
              );
            }
            rows.value = value.data;
          });
    };

    watch(
      () => $route.name,
      async (to) => {
        kindAPI.value = S(to).underscore().s;
        title.value = S(to).humanize().titleCase().s;
        kind.value = S(to).toLowerCase().camelize().s;
        fetchData();
      },
      { immediate: true },
    );

    onMounted(async () => await fetchData());

    const renderDate = (attributes) => {
      if (attributes.startDate && attributes.endDate) {
        return `${attributes.startDate.name}<br>${attributes.endDate.name}`;
      }
      if (attributes.startDate) {
        return attributes.startDate.name;
      }
      return attributes.date.name;
    };

    const getLocaleData = (data) => (Array.isArray(data) ? data[0] : data);

    return {
      columns,
      filter,
      getLocaleData,
      loading,
      noData,
      pagination,
      renderDate,
      rows,
      title,
      visibleColumns,
    };
  },
});
</script>
