<template>
  <Page>
    <Library />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Library, Page } from "@/components";

export default defineComponent({
  name: "Library",
  components: {
    Library,
    Page,
  },
  setup() {
    useMeta({ title: "Library" });
  },
});
</script>
