<template>
  <div v-if="onlyTrue">
    <q-icon
      v-if="value"
      :name="trueIcon"
      :color="onlyTrueGreen ? trueColour : falseColour"
      :size="size"
    />
  </div>
  <div v-else>
    <q-icon
      :name="value ? trueIcon : falseIcon"
      :color="value ? trueColour : falseColour"
      :size="size"
    />
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "BooleanIcon",
  props: {
    onlyTrue: {
      type: Boolean,
      required: false,
      default: false,
    },
    onlyTrueGreen: {
      type: Boolean,
      required: false,
      default: true,
    },
    trueIcon: {
      type: String,
      required: false,
      default: "check_box",
    },
    falseIcon: {
      type: String,
      required: false,
      default: "disabled_by_default",
    },
    trueColour: {
      type: String,
      required: false,
      default: "green-7",
    },
    falseColour: {
      type: String,
      required: false,
      default: "red-6",
    },
    value: {
      type: Boolean,
      required: true,
    },
    size: {
      type: String,
      required: false,
      default: "xs",
    },
  },
});
</script>
