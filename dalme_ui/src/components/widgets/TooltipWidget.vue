<template>
  <q-tooltip
    class="bg-blue z-max"
    :anchor="anchor"
    :self="self"
    :offset="offset"
    v-if="showTips"
  >
    <slot />
    {{ text }}
  </q-tooltip>
</template>

<script>
import { defineComponent } from "vue";
import { useTooltips } from "@/use";

export default defineComponent({
  name: "TooltipWidget",
  props: {
    anchor: {
      type: String,
      default: () => "bottom middle",
    },
    self: {
      type: String,
      default: () => "top middle",
    },
    offset: {
      type: Array,
      default: () => [14, 14],
    },
    text: {
      type: String,
    },
  },
  setup() {
    const { showTips } = useTooltips();

    return { showTips };
  },
});
</script>
