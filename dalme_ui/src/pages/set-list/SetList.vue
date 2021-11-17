<template>
  <Page>
    <Sets />
  </Page>
</template>

<script>
import { defineComponent } from "vue";

import { Page, Sets } from "@/components";

export default defineComponent({
  name: "SetList",
  components: {
    Page,
    Sets,
  },
});
</script>
