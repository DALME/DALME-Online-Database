<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
        :columns="columns"
        :filter="filter"
        :loading="loading"
        :no-data-label="noData"
        :pagination="pagination"
        :rows="rows"
        :title="title"
        :title-class="{ 'text-h6': true }"
        row-key="id"
      >
        <template #top-right>
          <q-input v-model="filter" debounce="300" placeholder="Search" borderless dense>
            <template #append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>

        <template #body-cell-creators="props">
          <q-td :props="props">
            {{ formatCreators(props.value) }}
          </q-td>
        </template>
      </q-table>
    </q-card>
    <OpaqueSpinner :showing="loading" />
  </div>
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, onMounted, ref } from "vue";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components";
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
  name: "LibraryList",
  components: {
    OpaqueSpinner,
  },
  setup() {
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();

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
        (creator) => `${creator.creatorType}: ${creator.firstName} ${creator.lastName}`,
        creators,
      ).join(", ");

    const fetchData = async () => {
      const request = requests.library.getLibrary();
      await fetchAPI(request);
      if (success.value)
        await libraryListSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          columns.value = getColumns();
          rows.value = value;
          loading.value = false;
        });
    };

    onMounted(async () => await fetchData());

    return {
      columns,
      filter,
      formatCreators,
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
