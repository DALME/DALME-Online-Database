<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <TaskDetail />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { TaskDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Task",
  components: {
    SuspenseWithError,
    TaskDetail,
  },
});
</script>
