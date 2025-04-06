<template>
  <div
    ref="container"
    :class="`spinner-container ${position} ${adaptive ? 'adaptive' : ''}`"
    :style="style"
    v-if="showing"
  >
    <q-spinner-facebook
      v-if="type === 'facebook'"
      :size="cSize"
      :thickness="thickness"
      :color="color"
    />
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
import { computed } from "vue";
import { defineComponent, onMounted, ref, useTemplateRef } from "vue";

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
    containerHeight: Number,
    containerWidth: Number,
  },
  setup(props) {
    const container = useTemplateRef("container");
    const cSize = ref(props.size);
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
      if (props.adaptive) {
        cSize.value = `${container.value.clientWidth / 10}px`;
      }
      console.log(style.value);
    });

    return {
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
.spinner-container .adaptive {
  display: flex;
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
