<template>
  <template v-if="merge">
    <div :class="`icon-merge ${classes}`">
      <q-icon :name="mergeIcons[0]" :size="`${size + 4}px`" />
      <q-icon :name="mergeIcons[1]" :size="`${size - 2}px`" />
    </div>
  </template>
  <template v-else>
    <q-icon :class="classes" :name="icon" :size="`${size}px`" />
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

<style lang="scss" scoped>
.icon-merge {
  display: flex;
  align-items: center;
}
.icon-merge .q-icon:last-of-type {
  position: absolute;
  padding-left: 3px;
}
</style>
