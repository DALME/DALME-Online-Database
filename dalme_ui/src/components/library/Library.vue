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

        <template v-slot:body-cell-creators="props">
          <q-td :props="props">
            {{ formatCreators(props.value) }}
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { map, keys } from "ramda";
import { defineComponent, ref } from "vue";

import { requests } from "@/api";
import { libraryListSchema } from "@/schemas";
import { useAPI } from "@/use";

const columnMap = {
  key: "Key",
  title: "Title",
  itemType: "Type",
  date: "Date",
  creators: "Creators",
};

export default defineComponent({
  name: "Library",
  async setup(_, context) {
    const { success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No library entries found.";
    const title = "Library";
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

    const formatCreators = (creators) =>
      map(
        (creator) =>
          `${creator.creatorType}: ${creator.firstName} ${creator.lastName}`,
        creators,
      ).join(", ");

    const fetchData = async () => {
      const request = requests.library.getLibrary();
      await fetchAPI(request);
      if (success.value)
        await libraryListSchema
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
      formatCreators,
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
