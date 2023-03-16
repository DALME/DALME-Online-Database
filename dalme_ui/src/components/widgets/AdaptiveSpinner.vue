<template>
  <div ref="el" class="spinner-container" :style="spinnerStyle">
    <q-spinner-dots :size="spinnerSize" />
  </div>
</template>

<script>
import { computed, defineComponent, onMounted, ref } from "vue";

export default defineComponent({
  name: "AdaptiveSpinner",
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
    const el = ref(null);
    /* eslint-disable */
    const spinnerStyle = computed(
      () => `top: ${props.top}px; right: ${props.right}px; bottom: ${props.bottom}px; left: ${props.left}px`
    );
    /* eslint-enable */
    const spinnerSize = ref("2rem");

    onMounted(() => {
      spinnerSize.value = `${el.value.clientWidth / 10}px`;
    });

    return {
      el,
      spinnerSize,
      spinnerStyle,
    };
  },
});
</script>

<style lang="scss">
.spinner-container {
  position: relative;
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: center;
  justify-items: center;
  color: #5c5c5c2e;
}
</style>
