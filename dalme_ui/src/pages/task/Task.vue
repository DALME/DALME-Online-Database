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
import { useMeta } from "quasar";
import { defineComponent, provide } from "vue";

import { TaskDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Task",
  props: {
    objId: {
      type: String,
      required: true,
    },
  },
  components: {
    SuspenseWithError,
    TaskDetail,
  },
  setup(props) {
    useMeta({ title: `Task #${props.objId}` });
    provide("objId", props.objId);
  },
});
</script>
