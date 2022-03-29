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
        :loading="loading"
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
    <OpaqueSpinner :showing="loading" />
  </div>
</template>

<script>
import { map, keys } from "ramda";
import { defineComponent, onMounted, ref } from "vue";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
import { agentListSchema } from "@/schemas";
import { useAPI } from "@/use";

const columnMap = {
  standardName: "Standard Name",
  type: "Type",
  user: "User",
};

export default defineComponent({
  name: "Agents",
  components: {
    OpaqueSpinner,
  },
  setup() {
    const { apiInterface } = useAPI();

    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No agents found.";
    const title = "Agents";
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
      const request = requests.agents.getAgents();
      await fetchAPI(request);
      if (success.value)
        await agentListSchema
          .validate(data.value.data, { stripUnknown: true })
          .then((value) => {
            columns.value = getColumns();
            rows.value = value;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    return {
      columns,
      filter,
      loading,
      noData,
      pagination,
      rows,
      title,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-table tbody td {
  white-space: normal;
}
</style>
