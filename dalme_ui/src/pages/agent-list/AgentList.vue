<template>
  <Page>
    <Agents />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Agents, Page } from "@/components";

export default defineComponent({
  name: "AgentList",
  components: {
    Agents,
    Page,
  },
  setup() {
    useMeta({ title: "Agents" });
  },
});
</script>
