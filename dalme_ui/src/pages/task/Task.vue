<template>
  <Page>
    <TaskDetail />
  </Page>
</template>

<script>
import { defineComponent } from "vue";

import { Page, TaskDetail } from "@/components";

export default defineComponent({
  name: "Task",
  components: {
    Page,
    TaskDetail,
  },
});
</script>
