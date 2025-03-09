<template>
  <q-table
    :columns="columns"
    :filter="filter"
    :loading="loading"
    :no-data-label="noData"
    :rows="rows"
    @request="onRequest"
    v-model:pagination="pagination"
    row-key="id"
    class="sticky-header"
  >
    <template v-slot:top>
      <q-item-section avatar>
        <q-avatar>
          <q-icon name="people" />
        </q-avatar>
      </q-item-section>
      <q-item-label class="text-weight-medium">
        Set Members ({{ memberCount }}, {{ publicMemberCount }} public)
      </q-item-label>
      <q-space />
      <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>

    <template v-slot:body-cell-name="props">
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

    <template v-slot:body-cell-isPublic="props">
      <q-td :props="props">
        <div class="col-8">
          <q-icon :name="props.value ? 'done' : 'close'" />
        </div>
      </q-td>
    </template>
  </q-table>
  <AdaptiveSpinner type="facebook" :showing="loading" thickness="3" />
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
  components: {
    AdaptiveSpinner,
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

<style lang="scss">
.q-table__top {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding-top: 8px;
  padding-bottom: 8px;
}
.q-table__bottom--nodata {
  border: 0;
}
</style>
