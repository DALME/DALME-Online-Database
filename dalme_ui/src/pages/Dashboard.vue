<template>
  <PageContainer>
    <template v-if="false">
      <TaskList :embedded="true" />
      <SetList :embedded="true" />
      <TicketList :embedded="true" />
    </template>
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { PageContainer, SetList, TaskList, TicketList } from "@/components";

export default defineComponent({
  name: "DashBoard",
  components: {
    PageContainer,
    SetList,
    TaskList,
    TicketList,
  },
  setup() {
    useMeta({ title: "Dashboard" });
  },
});
</script>
