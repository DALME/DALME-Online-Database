<template>
  <div ref="el" :class="`spinner-container ${position}`" :style="style" v-if="showing">
    <q-spinner-facebook v-if="type === 'facebook'" :thickness="thickness" :color="color" />
    <q-spinner-audio
      v-else-if="type === 'audio'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-bars
      v-else-if="type === 'bars'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-comment
      v-else-if="type === 'comment'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-cube
      v-else-if="type === 'cube'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-hourglass
      v-else-if="type === 'hourglass'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-ios v-else-if="type === 'ios'" :size="cSize" :thickness="thickness" :color="color" />
    <q-spinner-orbit
      v-else-if="type === 'orbit'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-oval
      v-else-if="type === 'oval'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-pie v-else-if="type === 'pie'" :size="cSize" :thickness="thickness" :color="color" />
    <q-spinner-puff
      v-else-if="type === 'puff'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-rings
      v-else-if="type === 'rings'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
    <q-spinner-dots v-else :size="cSize" :thickness="thickness" :color="color" />
  </div>
</template>

<script>
import { computed, defineComponent, onMounted, ref } from "vue";

export default defineComponent({
  name: "AdaptiveSpinner",
  props: {
    showing: {
      type: Boolean,
      default: true,
    },
    adaptive: {
      type: Boolean,
      default: true,
    },
    type: {
      type: String,
      default: "dots",
    },
    position: {
      type: String,
      default: "relative",
    },
    size: {
      type: String,
      default: "2rem",
    },
    color: {
      type: String,
      default: "currentColor",
    },
    thickness: {
      type: Number,
      default: 5,
    },
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
    const style = computed(
      () => `top: ${props.top}px; right: ${props.right}px; bottom: ${props.bottom}px; left: ${props.left}px`
    );
    /* eslint-enable */
    const cSize = ref(props.size);

    onMounted(() => {
      if (props.adaptive) {
        cSize.value = `${el.value.clientWidth / 10}px`;
      }
    });

    return {
      el,
      cSize,
      style,
    };
  },
});
</script>

<style lang="scss">
.spinner-container {
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: center;
  justify-items: center;
  color: #5c5c5c2e;
}
.spinner-container.relative {
  position: relative;
}
.spinner-container.absolute {
  position: absolute;
  background: inherit;
  top: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  left: 0 !important;
  z-index: 999;
}
.spinner-container .q-spinner {
  display: block;
}
</style>
