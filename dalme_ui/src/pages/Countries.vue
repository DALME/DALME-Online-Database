<template>
  <Page>
    <Countries />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Countries, Page } from "@/components";

export default defineComponent({
  name: "Countries",
  components: {
    Countries,
    Page,
  },
  setup() {
    useMeta({ title: "Countries" });
  },
});
</script>
