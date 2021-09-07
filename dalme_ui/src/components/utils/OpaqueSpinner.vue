<template>
  <q-inner-loading class="inner" :showing="showing">
    <q-spinner color="primary" size="3em" :thickness="6" />
  </q-inner-loading>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "OpaqueSpinner",
  props: {
    showing: {
      type: Boolean,
      required: true,
    },
  },
});
</script>

<style lang="scss">
.q-spinner {
  display: none;
}
</style>
