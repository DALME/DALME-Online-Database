<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <SourceDetail />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide } from "vue";

import { SourceDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Source",
  props: {
    objId: {
      type: String,
      required: true,
    },
  },
  components: {
    SuspenseWithError,
    SourceDetail,
  },
  setup(props) {
    useMeta({ title: `Source ${props.objId}` });
    provide("objId", props.objId);
  },
});
</script>
