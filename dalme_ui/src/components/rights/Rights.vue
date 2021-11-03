<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
        :title="title"
        :rows="rows"
        :columns="columns"
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
          <q-td :props="props" class="text-subtitle2">
            <router-link
              :to="{
                name: 'Rights',
                params: { id: props.row.id },
              }"
            >
              {{ props.value }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-publicDisplay="props">
          <q-td :props="props">
            <q-icon :name="props.value ? 'done' : 'close'" size="xs" />
          </q-td>
        </template>

        <template v-slot:body-cell-noticeDisplay="props">
          <q-td :props="props">
            <q-icon :name="props.value ? 'done' : 'close'" size="xs" />
          </q-td>
        </template>

        <template v-slot:body-cell-attachments="props">
          <q-td :props="props">
            <q-btn
              push
              @click="openURL(props.value.url)"
              :label="props.value.kind"
              target="_blank"
              color="white"
              size="sm"
              text-color="primary"
              v-if="props.value"
            >
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { openURL } from "quasar";
import { map, keys } from "ramda";
import { defineComponent, ref } from "vue";

import { requests } from "@/api";
import { rightsListSchema } from "@/schemas";
import { useAPI } from "@/use";

const columnMap = {
  name: "Name",
  rightsHolder: "Rights Holder",
  status: "Status",
  rights: "DALME Rights",
  publicDisplay: "Public Display",
  noticeDisplay: "Notice Display",
  attachments: "Attachments",
};

export default defineComponent({
  name: "Rights",
  async setup(_, context) {
    const { success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No rights found.";
    const title = "Rights";
    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

    const getColumns = () => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys(columnMap));
    };

    const fetchData = async () => {
      const request = requests.rights.getRights();
      await fetchAPI(request);
      if (success.value)
        await rightsListSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns();
            rows.value = value;
          });
    };

    await fetchData();

    return {
      columns,
      filter,
      openURL,
      noData,
      pagination,
      rows,
      title,
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
</style>
