<template>
  <q-table
    v-model:pagination="pagination"
    @request="onRequest"
    :columns="columns"
    :filter="filter"
    :loading="loading"
    :no-data-label="noData"
    :rows="rows"
    class="sticky-header"
    row-key="id"
  >
    <template #top>
      <q-item-section avatar>
        <q-avatar>
          <q-icon name="people" />
        </q-avatar>
      </q-item-section>
      <q-item-label class="text-weight-medium">
        Set Members ({{ memberCount }}, {{ publicMemberCount }} public)
      </q-item-label>
      <q-space />
      <q-input v-model="filter" debounce="300" placeholder="Search" borderless dense>
        <template #append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>

    <template #body-cell-name="props">
      <q-td :props="props">
        <router-link
          :to="{
            name: 'Source',
            params: { id: props.row.id },
          }"
        >
          {{ props.value }}
        </router-link>
      </q-td>
    </template>

    <template #body-cell-isPublic="props">
      <q-td :props="props">
        <div class="col-8">
          <q-icon :name="props.value ? 'done' : 'close'" />
        </div>
      </q-td>
    </template>
  </q-table>
  <AdaptiveSpinner :showing="loading" thickness="3" type="facebook" />
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, inject, ref } from "vue";

import { requests } from "@/api";
import { AdaptiveSpinner } from "@/components";
import { setMembersSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";

const columnMap = {
  id: "ID",
  name: "Name",
  isPublic: "Public",
};

export default defineComponent({
  name: "SetMembers",
  components: {
    AdaptiveSpinner,
  },
  props: {
    memberCount: {
      type: Number,
      required: true,
    },
    publicMemberCount: {
      type: Number,
      required: true,
    },
  },
  setup() {
    const { apiInterface } = useAPI();

    const { loading, success, data, fetchAPI } = apiInterface();
    const columns = ref([]);
    const rows = ref([]);
    const fieldMap = ref(null);

    const noData = "No members found.";

    const id = inject("id");

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

    const fetchData = async (query) => {
      rows.value = [];
      const request = requests.sets.getSetMembers(id.value, query);
      await fetchAPI(request);
      if (success.value)
        await setMembersSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          columns.value = getColumns();
          fieldMap.value = data.value.data.length ? keys(data.value.data[0]) : null;
          pagination.value.rowsNumber = value.count;
          rows.value.splice(0, rows.value.length, ...value.data);
          loading.value = false;
        });
    };

    const { filter, pagination, onRequest } = usePagination(fetchData);

    return {
      columns,
      filter,
      loading,
      onRequest,
      noData,
      pagination,
      rows,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-table__top {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding-top: 8px;
  padding-bottom: 8px;
}
.q-table__bottom--nodata {
  border: 0;
}
</style>
