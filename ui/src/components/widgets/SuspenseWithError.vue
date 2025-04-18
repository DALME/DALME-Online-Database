<template>
  <slot v-if="error" name="error">
    <div class="q-ma-md full-width full-height">
      <q-card class="flex flex-center q-ma-md">Something went wrong...</q-card>
    </div>
  </slot>
  <Suspense v-else>
    <template #default>
      <slot name="default"></slot>
    </template>
    <template #fallback>
      <div class="flex flex-center q-pa-lg">
        <q-spinner :thickness="6" color="primary" size="3em" />
      </div>
    </template>
  </Suspense>
</template>

<script>
import { defineComponent, onErrorCaptured, ref } from "vue";

import logger from "@/logger";

export default defineComponent({
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
});
</script>
