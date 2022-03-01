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
        <template v-if="!nothingOwned" v-slot:top-right>
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

        <template v-slot:no-data="{ message }">
          <div>{{ message }}</div>
        </template>

        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <router-link
              class="text-subtitle2"
              :to="{ name: 'Set', params: { id: props.row.id } }"
            >
              {{ props.row.name }}
            </router-link>
            <div class="q-mt-xs">{{ props.row.description }}</div>
            <q-badge outline color="blue-grey-10" class="q-my-sm">
              ENDPONT: {{ props.row.endpoint.toUpperCase() }}
            </q-badge>
          </q-td>
        </template>

        <template v-slot:body-cell-worksetProgress="props">
          <q-td :props="props">
            <q-circular-progress
              show-value
              color="teal"
              font-size="12px"
              size="50px"
              track-color="grey-3"
              :thickness="0.22"
              :value="props.value * 100"
            >
              {{ props.value * 100 }}%
            </q-circular-progress>
          </q-td>
        </template>
      </q-table>
    </q-card>
    <OpaqueSpinner :showing="loading" />
  </div>
</template>

<script>
import { openURL } from "quasar";
import { map, keys } from "ramda";
import { defineComponent, onMounted, ref } from "vue";
import { useStore } from "vuex";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
import { setListSchema } from "@/schemas";
import { useAPI } from "@/use";

const columnMap = {
  name: "Workset",
  worksetProgress: "Progress",
};

export default defineComponent({
  name: "Worksets",
  props: {
    embedded: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    OpaqueSpinner,
  },
  setup(props, context) {
    const $store = useStore();
    const { loading, success, data, fetchAPI } = useAPI(context);

    const columns = ref([]);
    const rows = ref([]);
    const filter = ref("");
    const nothingOwned = ref(false);

    const noData = "No owned worksets.";
    const title = "My Worksets";
    const rowsPerPage = 5;
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
      const request = requests.sets.getUserWorksets(
        $store.getters["auth/userId"],
      );
      await fetchAPI(request);
      if (success.value)
        await setListSchema("worksets")
          .validate(data.value, { stripUnknown: true })
          .then(async (value) => {
            if (value.length > 0) {
              columns.value = getColumns();
            } else {
              nothingOwned.value = true;
            }
            rows.value = value;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    return {
      columns,
      filter,
      noData,
      openURL,
      nothingOwned,
      pagination,
      rows,
      title,
      loading,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-table tbody td {
  white-space: normal;
}
</style>
