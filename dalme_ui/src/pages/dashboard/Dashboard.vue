<template>
  <q-page class="flex flex-center">
    <SuspenseWithError>
      <template #default>
        <Tickets />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { Tickets } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Dashboard",
  components: {
    SuspenseWithError,
    Tickets,
  },
});
</script>
