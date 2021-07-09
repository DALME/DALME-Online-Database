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
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { isEmpty, keys, map } from "ramda";
import { useMeta } from "quasar";
import S from "string";
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";

import { requests } from "@/api";
import { sourceListSchema } from "@/schemas";
import { useAPI } from "@/use";

import { columnsByKind } from "./columns";

export default defineComponent({
  name: "Sources",
  async setup() {
    const $router = useRouter();

    // TODO: Let's try a ref + inject on SourceRoot to do this.
    const routeName = $router.currentRoute.value.name;
    const kind = S(routeName).camelize().s.toLowerCase(); // TODO: This is wrong?
    const title = S(routeName).humanize().titleCase().s;

    useMeta({ title });
    const { success, data, fetchAPI } = useAPI();

    const columns = ref([]);
    // const visibleColumns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No sources found.";
    const pagination = { rowsPerPage: 20 };

    const getColumns = (keys) => {
      const columnMap = columnsByKind(kind);
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, keys);
    };

    const request = requests.sources.getSources(kind);
    await fetchAPI(request);
    if (success.value)
      await sourceListSchema(kind)
        .validate(data.value, { stripUnknown: true })
        .then((value) => {
          if (!isEmpty(value)) {
            columns.value = getColumns(keys(columnsByKind(kind)));
          }
          rows.value = value.data;
        });

    return { columns, filter, noData, pagination, rows, title };
  },
});
</script>
