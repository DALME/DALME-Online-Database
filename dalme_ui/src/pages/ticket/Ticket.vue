<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <TicketDetail />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { defineComponent, provide } from "vue";

import { TicketDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Ticket",
  components: {
    SuspenseWithError,
    TicketDetail,
  },
  setup() {
    provide("model", "Ticket");
  },
});
</script>
