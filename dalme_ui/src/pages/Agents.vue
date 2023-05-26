<template>
  <PageContainer>
    <AgentList />
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { AgentList, PageContainer } from "@/components";

export default defineComponent({
  name: "AgentsPageContainer",
  components: {
    AgentList,
    PageContainer,
  },
  setup() {
    useMeta({ title: "Agents" });
  },
});
</script>
