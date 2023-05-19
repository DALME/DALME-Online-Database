<template>
  <Page>
    <Locales />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Locales, Page } from "@/components";

export default defineComponent({
  name: "Locales",
  components: {
    Locales,
    Page,
  },
  setup() {
    useMeta({ title: "Locales" });
  },
});
</script>
