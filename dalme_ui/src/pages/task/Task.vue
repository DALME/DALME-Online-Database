<template>
  <Page>
    <div class="full-width full-height q-px-content-visual">
      <TaskDetail />
    </div>
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
