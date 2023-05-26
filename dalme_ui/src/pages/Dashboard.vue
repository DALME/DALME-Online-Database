<template>
  <PageContainer>
    <TaskList :embedded="true" />
    <WorksetWidget />
    <TicketList :embedded="true" />
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import {
  PageContainer,
  TaskList,
  TicketList,
  WorksetWidget,
} from "@/components";

export default defineComponent({
  name: "DashBoard",
  components: {
    PageContainer,
    TaskList,
    TicketList,
    WorksetWidget,
  },
  setup() {
    useMeta({ title: "Dashboard" });
    // throw new Error("Parameter is not a number!");
  },
});
</script>
