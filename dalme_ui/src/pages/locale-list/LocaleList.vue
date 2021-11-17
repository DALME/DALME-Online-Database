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
  name: "LocaleList",
  components: {
    Locales,
    Page,
  },
  setup() {
    useMeta({ title: "Locales" });
  },
});
</script>
