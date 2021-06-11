<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Tickets />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Tickets } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "TicketList",
  components: {
    SuspenseWithError,
    Tickets,
  },
  setup() {
    useMeta({ title: "Issue Tickets" });
  },
});
</script>
