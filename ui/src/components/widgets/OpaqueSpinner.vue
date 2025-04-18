<template>
  <q-inner-loading :showing="showing" class="inner">
    <q-spinner :thickness="6" color="primary" size="3em" />
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

<style lang="scss" scoped>
.q-spinner {
  display: none;
}
</style>
