<template>
  <q-page>
    <Tickets />
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Tickets } from "@/components";

export default defineComponent({
  name: "TicketList",
  components: {
    Tickets,
  },
  setup() {
    useMeta({ title: "Issue Tickets" });
  },
});
</script>
