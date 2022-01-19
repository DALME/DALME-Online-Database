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

        <template v-slot:body-cell-username="props">
          <q-td :props="props" class="text-subtitle2">
            <router-link
              :to="{
                name: 'User',
                params: { username: props.value },
              }"
            >
              {{ props.value }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-email="props">
          <q-td :props="props">
            <a :href="`mailto:${props.value}`">
              {{ props.value }}
            </a>
          </q-td>
        </template>

        <template v-slot:body-cell-isActive="props">
          <q-td :props="props">
            <q-icon :name="props.value ? 'done' : 'close'" size="xs" />
          </q-td>
        </template>

        <template v-slot:body-cell-isStaff="props">
          <q-td :props="props">
            <q-icon :name="props.value ? 'done' : 'close'" size="xs" />
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
import { userListSchema } from "@/schemas";
import { useAPI } from "@/use";

const columnMap = {
  id: "ID",
  fullName: "Full Name",
  email: "Email",
  username: "Username",
  lastLogin: "Last Login",
  isActive: "Active",
  isStaff: "Staff",
};

export default defineComponent({
  name: "Users",
  components: {
    OpaqueSpinner,
  },
  setup(_, context) {
    const { loading, success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No users found.";
    const title = "Users";
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
      const request = requests.users.getUsers();
      await fetchAPI(request);
      if (success.value)
        await userListSchema
          .validate(data.value, { stripUnknown: true })
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

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
</style>
