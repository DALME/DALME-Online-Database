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
  </div>
</template>

<script>
import { head, isEmpty, map, keys, reverse } from "ramda";
import { defineComponent, ref } from "vue";

import { requests } from "@/api";
import { userListSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Users",
  async setup() {
    const { success, data, fetchAPI } = useAPI();

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No users found.";
    const title = "Users";
    const rowsPerPage = 25;
    const pagination = { rowsPerPage };

    const getColumns = (keys) => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: {
          id: "ID",
          fullName: "Full Name",
          email: "Email",
          username: "Username",
          lastLogin: "Last Login",
          isActive: "Active",
          isStaff: "Staff",
        }[key],
        name: key,
        sortable: true,
      });
      return reverse(map(toColumn, keys));
    };

    const fetchData = async () => {
      const request = requests.users.getUsers();
      await fetchAPI(request);
      if (success.value)
        await userListSchema
          .validate(data.value, { stripUnknown: true })
          .then(async (value) => {
            if (!isEmpty(value)) {
              columns.value = getColumns(keys(head(value)));
            }
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
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
</style>
