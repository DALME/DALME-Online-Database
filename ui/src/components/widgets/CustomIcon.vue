<template>
  <template v-if="merge">
    <div :class="`icon-merge ${classes}`">
      <q-icon :size="`${size + 4}px`" :name="mergeIcons[0]" />
      <q-icon :size="`${size - 2}px`" :name="mergeIcons[1]" />
    </div>
  </template>
  <template v-else>
    <q-icon :size="`${size}px`" :name="icon" :class="classes" />
  </template>
</template>

<script>
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "CustomIcon",
  props: {
    icon: {
      type: String,
      required: true,
    },
    size: {
      type: Number,
      required: false,
      default: 12,
    },
    classes: {
      type: String,
      required: false,
      default: "",
    },
  },
  setup(props) {
    const merge = computed(() => props.icon.startsWith("merge"));
    const mergeIcons = computed(() => (merge.value ? props.icon.split(" ").slice(1) : null));
    return {
      merge,
      mergeIcons,
    };
  },
});
</script>

<style lang="scss">
.icon-merge {
  display: flex;
  align-items: center;
}
.icon-merge .q-icon:last-of-type {
  position: absolute;
  padding-left: 3px;
}
</style>
