<template>
  <div class="q-pa-md">
    <q-card>
      <q-table
        title="My Issue Tickets"
        :rows="rows"
        :columns="columns"
        :no-data-label="noData"
        :filter="filter"
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
      </q-table>
    </q-card>

    <q-card class="modal">
      <q-btn
        style="background: #ff0080; color: white"
        label="TEST REAUTH"
        @click="testModal()"
      />
    </q-card>
  </div>
</template>

<script>
import { head, isEmpty, map, keys, reverse } from "ramda";
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";

import { modalLoginUrl, requests } from "@/api";
import { ticketListSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Tickets",
  async setup() {
    const $store = useStore();
    const { success, data, fetchAPI } = useAPI();

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");
    const noData = "No tickets found.";

    const getColumns = (keys) => {
      const labels = {
        id: "ID",
        file: "Attachments",
        tag: "Tags",
        subject: "Ticket",
        commentCount: "Comments",
      };
      const toColumn = (key) => {
        return {
          name: key,
          field: key,
          label: labels[key],
          align: "left",
          sortable: true,
          required: key === "id" ? true : false,
        };
      };
      return reverse(map(toColumn, keys));
    };

    const userId = $store.getters["auth/userId"];
    await fetchAPI(requests.tickets.userTickets(userId));
    if (success)
      ticketListSchema
        .validate(data.value, { stripUnknown: true })
        .then((value) => {
          if (!isEmpty(value.results))
            columns.value = getColumns(keys(head(value.results)));
          rows.value = value.results;
        });

    const testModal = async () => {
      const request = new Request(modalLoginUrl);
      await fetchAPI(request);
    };

    return {
      columns,
      filter,
      noData,
      rows,
      testModal,
    };
  },
});
</script>

<style scoped lang="scss">
.modal {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding: 2rem;
}
</style>
