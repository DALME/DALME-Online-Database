<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Sets />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Sets } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "TicketList",
  components: {
    SuspenseWithError,
    Sets,
  },
  setup() {
    useMeta({ title: "Sets" });
  },
});
</script>
