<template>
  <Page>
    <Languages />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Languages, Page } from "@/components";

export default defineComponent({
  name: "Languages",
  components: {
    Languages,
    Page,
  },
  setup() {
    useMeta({ title: "Languages" });
  },
});
</script>
