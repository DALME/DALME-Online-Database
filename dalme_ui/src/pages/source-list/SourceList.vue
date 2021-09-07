<template>
  <q-page>
    <Sources />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { Sources } from "@/components";

export default defineComponent({
  name: "SourceList",
  components: {
    Sources,
  },
});
</script>
