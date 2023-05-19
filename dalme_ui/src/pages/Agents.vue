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
  name: "Agents",
  components: {
    Agents,
    Page,
  },
  setup() {
    useMeta({ title: "Agents" });
  },
});
</script>
