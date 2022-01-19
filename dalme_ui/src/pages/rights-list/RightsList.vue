<template>
  <Page>
    <Rights />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Page, Rights } from "@/components";

export default defineComponent({
  name: "RightsList",
  components: {
    Page,
    Rights,
  },
  setup() {
    useMeta({ title: "Issue Rights" });
  },
});
</script>
