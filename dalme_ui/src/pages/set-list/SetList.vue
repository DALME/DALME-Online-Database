<template>
  <q-page>
    <Sets />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { Sets } from "@/components";

export default defineComponent({
  name: "SetList",
  components: {
    Sets,
  },
});
</script>
