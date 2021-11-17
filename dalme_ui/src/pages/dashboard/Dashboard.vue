<template>
  <Page>
    <Tasks :embedded="true" />
    <Tickets :embedded="true" />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Page, Tasks, Tickets } from "@/components";

export default defineComponent({
  name: "Dashboard",
  components: {
    Page,
    Tasks,
    Tickets,
  },
  setup() {
    useMeta({ title: "Dashboard" });
  },
});
</script>
