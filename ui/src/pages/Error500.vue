<template>
  <div class="fullscreen bg-blue text-white text-center q-ma-md flex flex-center">
    <div>
      <div style="font-size: 30vh">500</div>

      <div class="text-h2" style="opacity: 0.4">Something went wrong...</div>

      <q-btn
        :to="{ name: 'Home' }"
        class="q-mt-xl"
        color="white"
        label="Go Home"
        text-color="blue"
        no-caps
        unelevated
      />
    </div>
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

export default defineComponent({
  name: "Error500PageContainer",
  setup() {
    useMeta({ title: "500" });
  },
});
</script>
