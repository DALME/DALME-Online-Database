<template>
  <div
    v-if="showing"
    ref="container"
    :class="`spinner-container ${position} ${adaptive ? 'adaptive' : ''}`"
    :style="style"
  >
    <q-spinner-facebook
      v-if="type === 'facebook'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-audio
      v-else-if="type === 'audio'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-bars
      v-else-if="type === 'bars'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-comment
      v-else-if="type === 'comment'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-cube
      v-else-if="type === 'cube'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-hourglass
      v-else-if="type === 'hourglass'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-ios v-else-if="type === 'ios'" :color="color" :size="cSize" :thickness="thickness" />
    <q-spinner-orbit
      v-else-if="type === 'orbit'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-oval
      v-else-if="type === 'oval'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-pie v-else-if="type === 'pie'" :color="color" :size="cSize" :thickness="thickness" />
    <q-spinner-puff
      v-else-if="type === 'puff'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-rings
      v-else-if="type === 'rings'"
      :color="color"
      :size="cSize"
      :thickness="thickness"
    />
    <q-spinner-dots v-else :color="color" :size="cSize" :thickness="thickness" />
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
      default: false,
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
      required: false,
      default: null,
    },
    color: {
      type: String,
      default: "currentColor",
    },
    thickness: {
      type: [Number, String],
      default: 5,
    },
    top: {
      type: [Number, String],
      default: 0,
    },
    right: {
      type: [Number, String],
      default: 0,
    },
    bottom: {
      type: [Number, String],
      default: 0,
    },
    left: {
      type: [Number, String],
      default: 0,
    },
    containerHeight: {
      type: [Number, String],
      required: false,
      default: null,
    },
    containerWidth: {
      type: [Number, String],
      required: false,
      default: null,
    },
  },
  setup(props) {
    const cSize = ref(props.size || "2rem");
    const style = computed(() => {
      let result = "";
      if (props.top) result += `top: ${props.top}px;`;
      if (props.right) result += `right: ${props.right}px;`;
      if (props.bottom) result += `bottom: ${props.bottom}px;`;
      if (props.left) result += `left: ${props.left}px;`;
      if (props.containerHeight) result += `height: ${props.containerHeight}px;`;
      if (props.containerWidth) result += `width: ${props.containerWidth}px;`;
      return result;
    });

    onMounted(() => {
      if (props.adaptive && !props.size) {
        cSize.value = "50%";
      }
    });

    return {
      cSize,
      style,
    };
  },
});
</script>

<style lang="scss" scoped>
.spinner-container {
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: center;
  justify-items: center;
  color: #5c5c5c2e;
}
.spinner-container.adaptive {
  display: flex;
  height: 100%;
  width: 100%;
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
