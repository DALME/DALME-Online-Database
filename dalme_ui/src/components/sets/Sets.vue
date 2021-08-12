<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table> </q-table>
    </q-card>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";

// import { useAPI } from "@/use";

export default defineComponent({
  name: "Sets",
  async setup() {
    // const { success, data, fetchAPI } = useAPI();

    const columns = ref([]);
    const visibleColumns = ref(null);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No sets found.";
    const title = "Sets";
    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

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
