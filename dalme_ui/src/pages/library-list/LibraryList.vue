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
  name: "LibraryList",
  components: {
    Library,
    Page,
  },
  setup() {
    useMeta({ title: "Library" });
  },
});
</script>
