<template>
  <q-table
    v-if="locations.length > 0"
    :columns="columns"
    :filter="filter"
    :no-data-label="noData"
    :pagination="pagination"
    :rows="locations"
    :rows-per-page-options="[0]"
    class="sticky-header"
    row-key="id"
    table-colspan="3"
    dense
    flat
    wrap-cells
  >
    <template #body-cell-name="props">
      <q-td :props="props">
        <span v-html="props.value" />
      </q-td>
    </template>
  </q-table>
  <q-separator />
  <MapWidget :targets="targets" />
</template>

<script>
import { computed, defineComponent, inject, onBeforeMount, ref } from "vue";

import { MapWidget } from "@/components";
import { getColumns } from "@/utils";

import { columnMap } from "./locationColumns";

export default defineComponent({
  name: "RecordLocations",
  components: { MapWidget },
  props: {
    targets: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const columns = ref(getColumns(columnMap));
    const filter = inject("cardFilter");
    const noData = "No locations associated with this record.";
    const pagination = { rowsPerPage: 10 }; // 0 = all rows
    const locations = computed(() => {
      const locs = [];
      props.targets.forEach((target) => {
        const isPlace = target.entity === "place";
        const type = isPlace
          ? target.location && target.location.locationType === "Locale"
            ? "Place (Locale)"
            : "Place (?)"
          : "Locale (Attribute)";
        const detail = isPlace
          ? target.location && target.location.locationType === "Locale"
            ? target.location.attributes[0].value.name +
              ", " +
              target.location.attributes[0].value.administrativeRegion +
              ", " +
              target.location.attributes[0].value.country.name
            : null
          : target.value.administrativeRegion + ", " + target.value.country.name;
        const geometry = isPlace
          ? target.location && target.location.locationType === "Locale"
            ? "Point(" +
              target.location.attributes[0].value.latitude +
              ", " +
              target.location.attributes[0].value.longitude +
              ")"
            : "?"
          : "Point(" + target.value.latitude + ", " + target.value.longitude + ")";
        locs.push({
          name: isPlace ? target.name : target.value.name,
          type: type,
          detail: detail,
          geometry: geometry,
          attestationCount: isPlace ? target.attestationCount : null,
          recordAttestationCount: isPlace ? target.recordAttestationCount : null,
        });
      });
      return locs;
    });

    onBeforeMount(() => {
      console.log("RecordLocations onBeforeMount", props.targets);
    });

    return {
      columns,
      filter,
      noData,
      pagination,
      locations,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-table__top {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding: 0;
}
.q-table__bottom--nodata {
  border: 0;
}
</style>
