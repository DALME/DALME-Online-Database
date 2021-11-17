<template>
  <Page>
    <Tickets />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Page, Tickets } from "@/components";

export default defineComponent({
  name: "TicketList",
  components: {
    Page,
    Tickets,
  },
  setup() {
    useMeta({ title: "Issue Tickets" });
  },
});
</script>
