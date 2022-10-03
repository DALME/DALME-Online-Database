<template>
  <Page>
    <div class="full-width full-height q-px-content-visual">
      <TicketDetail />
    </div>
  </Page>
</template>

<script>
import { defineComponent, provide } from "vue";

import { Page, TicketDetail } from "@/components";

export default defineComponent({
  name: "Ticket",
  components: {
    Page,
    TicketDetail,
  },
  setup() {
    provide("model", "Ticket");
  },
});
</script>
