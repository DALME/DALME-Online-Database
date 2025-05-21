<template>
  <q-tooltip v-if="showTips" :anchor="anchor" :offset="offset" :self="self" class="bg-blue z-max">
    <slot />
    {{ text }}
  </q-tooltip>
</template>

<script>
import { defineComponent } from "vue";

import { Preferences } from "@/models";

export default defineComponent({
  name: "ToolTip",
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
      required: false,
      default: null,
    },
  },
  setup() {
    return { showTips: Preferences.get("tooltipsOn") };
  },
});
</script>
