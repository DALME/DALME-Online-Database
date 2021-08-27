<template>
  <q-page>
    <SetDetail />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { SetDetail } from "@/components";

export default defineComponent({
  name: "Set",
  components: {
    SetDetail,
  },
});
</script>
