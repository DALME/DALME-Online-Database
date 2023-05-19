<template>
  <Page>
    <Places />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Page, Places } from "@/components";

export default defineComponent({
  name: "Places",
  components: {
    Page,
    Places,
  },
  setup() {
    useMeta({ title: "Places" });
  },
});
</script>
