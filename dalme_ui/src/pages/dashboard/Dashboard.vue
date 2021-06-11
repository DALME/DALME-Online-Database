<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Tasks :embedded="true" />
      </template>
    </SuspenseWithError>
    <SuspenseWithError>
      <template #default>
        <Tickets :embedded="true" />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Tasks, Tickets } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Dashboard",
  components: {
    SuspenseWithError,
    Tasks,
    Tickets,
  },
  setup() {
    useMeta({ title: "Dashboard" });
  },
});
</script>
