<template>
  <Page>
    <SuspenseWithError>
      <template #default>
        <TaskDetail />
      </template>
    </SuspenseWithError>
  </Page>
</template>

<script>
import { defineComponent } from "vue";

import { Page, TaskDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Task",
  components: {
    Page,
    SuspenseWithError,
    TaskDetail,
  },
});
</script>
