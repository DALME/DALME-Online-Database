<template>
  <slot v-if="error" name="error">Something went wrong...</slot>
  <Suspense v-else>
    <template #default>
      <slot name="default"></slot>
    </template>
    <template #fallback>
      <Spinner />
    </template>
  </Suspense>
</template>

<script>
import { defineComponent, ref, onErrorCaptured } from "vue";

import { Spinner } from "@/components/utils";
import logger from "@/logger";

export default defineComponent({
  name: "SuspenseWithError",
  components: {
    Spinner,
  },
  setup() {
    const error = ref(null);

    onErrorCaptured((e) => {
      error.value = e;
      logger.error(e);
      return true;
    });

    return { error };
  },
});
</script>
