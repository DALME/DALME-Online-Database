<template>
  <PageContainer>
    <TaskList :embedded="true" />
    <SetList :embedded="true" />
    <TicketList :embedded="true" />
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { PageContainer, TaskList, TicketList, SetList } from "@/components";

export default defineComponent({
  name: "DashBoard",
  components: {
    PageContainer,
    TaskList,
    TicketList,
    SetList,
  },
  setup() {
    useMeta({ title: "Dashboard" });
    // throw new Error("Parameter is not a number!");
  },
});
</script>
