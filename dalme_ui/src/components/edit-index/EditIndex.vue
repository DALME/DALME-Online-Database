<template>
  <q-drawer bordered class="bg-grey-3" side="right" v-model="show">
    <q-scroll-area class="fit">
      <WindowIndex />
      <InlineIndex />
    </q-scroll-area>
  </q-drawer>
</template>

<script>
import { computed, defineComponent, provide, ref } from "vue";

import { InlineIndex, WindowIndex } from "@/components";

export default defineComponent({
  name: "Transport",
  components: {
    InlineIndex,
    WindowIndex,
  },
  setup() {
    const inlineIndexShow = ref(false);
    const windowIndexShow = ref(false);

    provide("inlineIndexShow", inlineIndexShow);
    provide("windowIndexShow", windowIndexShow);

    const show = computed({
      get: () => inlineIndexShow.value || windowIndexShow.value,
      set: () => inlineIndexShow.value || windowIndexShow.value,
    });

    return {
      show,
    };
  },
});
</script>
