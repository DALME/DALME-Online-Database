<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Sources />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { defineComponent, provide } from "vue";

import { Sources } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "SourceList",
  components: {
    SuspenseWithError,
    Sources,
  },
  setup(props) {
    provide("kind", props.kind);
  },
});
</script>
