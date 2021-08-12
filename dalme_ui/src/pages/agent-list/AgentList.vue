<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Agents />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Agents } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "AgentList",
  components: {
    SuspenseWithError,
    Agents,
  },
  setup() {
    useMeta({ title: "Agents" });
  },
});
</script>
