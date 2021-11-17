<template>
  <Page>
    <SuspenseWithError>
      <template #default>
        <TicketDetail />
      </template>
    </SuspenseWithError>
  </Page>
</template>

<script>
import { defineComponent, provide } from "vue";

import { Page, TicketDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Ticket",
  components: {
    Page,
    SuspenseWithError,
    TicketDetail,
  },
  setup() {
    provide("model", "Ticket");
  },
});
</script>
