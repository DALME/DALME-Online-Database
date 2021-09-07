<template>
  <q-table
    :columns="columns"
    :filter="filter"
    :loading="loading"
    :no-data-label="noData"
    :rows="rows"
    @request="onRequest"
    row-key="id"
    v-model:pagination="pagination"
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
          :to="{
            name: 'Source',
            params: { objId: props.row.objId },
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

  <Spinner :showing="loading" />
</template>

<script>
import { keys, map } from "ramda";
import { defineComponent, ref } from "vue";

import { requests } from "@/api";
import { Spinner } from "@/components/utils";
import { setMembersSchema } from "@/schemas";
import { useAPI, usePagination } from "@/use";

export default defineComponent({
  name: "SetMembers",
  props: {
    objId: {
      type: String,
      required: true,
    },
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
    Spinner,
  },
  setup(props, context) {
    const { loading, success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const rows = ref([]);
    const fieldMap = ref(null);

    const noData = "No members found.";

    const getColumns = () => {
      const columnMap = {
        objId: "ID",
        name: "Name",
        isPublic: "Public",
      };
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: columnMap[key],
        name: key,
        sortable: true,
      });
      return map(toColumn, ["objId", "name", "isPublic"]);
    };
    columns.value = getColumns();

    const fetchData = async (q) => {
      rows.value = [];
      const request = requests.sets.getSetMembers(props.objId, q);
      await fetchAPI(request);
      if (success.value)
        await setMembersSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            fieldMap.value = data.value.data.length
              ? keys(data.value.data[0])
              : null;
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
