<template>
  <q-inner-loading class="inner" :showing="showing">
    <q-spinner size="2em" :thickness="3" />
  </q-inner-loading>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "Spinner",
  props: {
    showing: {
      type: Boolean,
      required: true,
    },
  },
});
</script>
