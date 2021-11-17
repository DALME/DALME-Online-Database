<template>
  <Page>
    <SuspenseWithError>
      <template #default>
        <Agents />
      </template>
    </SuspenseWithError>
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Agents, Page } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "AgentList",
  components: {
    SuspenseWithError,
    Agents,
    Page,
  },
  setup() {
    useMeta({ title: "Agents" });
  },
});
</script>
