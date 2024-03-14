<template>
  <div class="spinner-container" :style="spinnerStyle">
    <q-spinner-facebook size="2em" :thickness="3" />
  </div>
</template>

<script>
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "SimpleSpinner",
  props: {
    top: {
      type: Number,
      default: 0,
    },
    right: {
      type: Number,
      default: 0,
    },
    bottom: {
      type: Number,
      default: 0,
    },
    left: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    /* eslint-disable */
    const spinnerStyle = computed(
      () =>
        `top: ${props.top}px; right: ${props.right}px; bottom: ${props.bottom}px; left: ${props.left}px`,
    );
    /* eslint-enable */

    return { spinnerStyle };
  },
});
</script>

<style lang="scss">
.spinner-container {
  position: absolute;
}
</style>
