<template>
  <q-page>
    <FormModal />
    <slot></slot>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { FormModal } from "@/components";

export default defineComponent({
  name: "Page",
  components: {
    FormModal,
  },
});
</script>
