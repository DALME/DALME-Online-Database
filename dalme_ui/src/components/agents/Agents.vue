<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
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

        <template v-slot:body-cell-standardName="props">
          <q-td :props="props" v-html="props.value"> </q-td>
        </template>

        <template v-slot:body-cell-type="props">
          <q-td :props="props">
            {{ props.value.name }}
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { filter as rFilter, head, isEmpty, map, keys, reverse } from "ramda";
import { defineComponent, ref } from "vue";

import { requests } from "@/api";
import { agentListSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Agents",
  async setup() {
    const { success, data, fetchAPI } = useAPI();

    const columns = ref([]);
    const visibleColumns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No agents found.";
    const title = "Agents";
    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

    const getColumns = (keys) => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: {
          standardName: "Standard Name",
          type: "Type",
          user: "User",
        }[key],
        name: key,
        sortable: true,
      });
      return reverse(map(toColumn, keys));
    };

    const fetchData = async () => {
      const request = requests.agents.getAgents();
      await fetchAPI(request);
      if (success.value)
        await agentListSchema
          .validate(data.value.data, { stripUnknown: true })
          .then(async (value) => {
            if (!isEmpty(value)) {
              columns.value = getColumns(keys(head(value)));
            }
            visibleColumns.value = map(
              (column) => column.field,
              rFilter(
                (column) => !["id"].includes(column.field),
                columns.value,
              ),
            );
            rows.value = value;
          });
    };

    await fetchData();

    return {
      columns,
      filter,
      noData,
      pagination,
      rows,
      title,
      visibleColumns,
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
</style>
