<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-table
        :title="title"
        :rows="rows"
        :columns="columns"
        :visible-columns="visibleColumns || columns"
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

        <template v-slot:body-cell-tags="props">
          <q-td :props="props">
            <q-badge v-if="props.value" outline color="primary">
              {{ props.value }}
            </q-badge>
          </q-td>
        </template>

        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-btn
              round
              :color="props.value ? 'green' : 'red'"
              text-color="white"
              :icon="props.value ? 'check_circle_outline' : 'error'"
              size="xs"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-subject="props">
          <q-td :props="props">
            <router-link
              class="text-subtitle2"
              :to="{ name: 'Ticket', params: { objId: props.row.id } }"
            >
              {{ props.value }}
            </router-link>
          </q-td>
        </template>

        <template v-slot:body-cell-file="props">
          <q-td :props="props">
            <q-btn
              push
              @click="openURL(props.value.source)"
              target="_blank"
              label="file"
              color="white"
              text-color="primary"
              v-if="props.value"
              size="sm"
            >
            </q-btn>
          </q-td>
        </template>

        <template v-slot:body-cell-commentCount="props">
          <q-td :props="props">
            <q-btn
              dense
              flat
              round
              icon="comment"
              class="q-ml-md"
              size="sm"
              v-if="props.value"
            >
              <q-badge color="red" transparent floating rounded>
                {{ props.value }}
              </q-badge>
            </q-btn>
          </q-td>
        </template>

        <template v-slot:body-cell-creationUser="props">
          <q-td :props="props">
            {{ props.value.fullName }}
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
import { openURL } from "quasar";
import {
  filter as rFilter,
  head,
  isEmpty,
  isNil,
  map,
  keys,
  reverse,
} from "ramda";
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";

import { requests } from "@/api";
import { attachmentSchema, ticketListSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Tickets",
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  async setup(props) {
    const $store = useStore();
    const { success, data, fetchAPI } = useAPI();

    const columns = ref([]);
    const visibleColumns = ref(null);
    const rows = ref([]);
    const filter = ref("");

    const noData = "No tickets found.";
    const title = props.embedded ? "My Issue Tickets" : "Issue Tickets";
    const rowsPerPage = props.embedded ? 5 : 25;
    const pagination = { rowsPerPage };

    const getColumns = (keys) => {
      const toColumn = (key) => ({
        align: "left",
        field: key,
        label: {
          id: "ID",
          status: "Status",
          file: "Attachments",
          tags: "Tags",
          subject: "Ticket",
          commentCount: "Comments",
          creationUser: "Created by",
          creationTimestamp: "Created on",
          closingDate: "Closed on",
        }[key],
        name: key,
        sortable: true,
      });
      return reverse(map(toColumn, keys));
    };

    const filterVisibleColumns = (columns) => {
      const exclude = [
        "creationUser",
        "creationTimestamp",
        "closingDate",
        "description",
        "commentCount",
      ];
      if (props.embedded) {
        return map(
          (column) => column.field,
          rFilter((column) => !exclude.includes(column.field), columns),
        );
      }
      return map(
        (column) => column.field !== "description" && column.field,
        columns,
      );
    };

    const resolveAttachments = async (tickets) => {
      const resolveAttachment = async (ticket) => {
        if (!isNil(ticket.file)) {
          const response = await fetch(
            requests.attachments.getAttachment(ticket.file),
          );
          if (response.status === 200) {
            const data = await response.json();
            await attachmentSchema
              .validate(data, { stripUnknown: true })
              .then((value) => (ticket.file = value));
          }
        }
        return ticket;
      };
      return Promise.all(map(resolveAttachment, tickets));
    };

    const fetchData = async () => {
      const request = props.embedded
        ? requests.tickets.userTickets($store.getters["auth/userId"])
        : requests.tickets.getTickets();
      await fetchAPI(request);
      if (success.value)
        await ticketListSchema
          .validate(data.value, { stripUnknown: true })
          .then(async (value) => {
            if (!isEmpty(value.results)) {
              columns.value = getColumns(keys(head(value.results)));
              visibleColumns.value = filterVisibleColumns(columns.value);
            }
            rows.value = await resolveAttachments(value.results);
          });
    };

    await fetchData();

    return {
      columns,
      filter,
      noData,
      openURL,
      pagination,
      rows,
      title,
      visibleColumns,
    };
  },
});
</script>

<style lang="scss">
.q-table tbody td {
  white-space: normal;
}
</style>
