<template>
  <slot v-if="error" name="error"></slot>
  <Suspense v-else>
    <template #default>
      <slot name="default"></slot>
    </template>
    <template #fallback>
      <slot name="fallback"></slot>
    </template>
  </Suspense>
</template>

<script>
import { ref, onErrorCaptured } from "vue";
import logger from "@/logger";

export default {
  name: "SuspenseWithError",
  setup() {
    const error = ref(null);

    onErrorCaptured((e) => {
      error.value = e;
      logger.error(e);
      return true;
    });

    return { error };
  },
};
</script>
