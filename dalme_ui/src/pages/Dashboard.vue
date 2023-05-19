<template>
  <Page>
    <Tasks :embedded="true" />
    <Worksets />
    <Tickets :embedded="true" />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { Page, Tasks, Tickets, Worksets } from "@/components";

export default defineComponent({
  name: "Dashboard",
  components: {
    Page,
    Tasks,
    Tickets,
    Worksets,
  },
  setup() {
    useMeta({ title: "Dashboard" });
    // throw new Error("Parameter is not a number!");
  },
});
</script>
