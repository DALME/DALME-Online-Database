<template>
  <q-page>
    <Tasks :embedded="true" />
    <Tickets :embedded="true" />
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Tasks, Tickets } from "@/components";

export default defineComponent({
  name: "Dashboard",
  components: {
    Tasks,
    Tickets,
  },
  setup() {
    useMeta({ title: "Dashboard" });
  },
});
</script>
