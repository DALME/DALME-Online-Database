<template>
  <div v-if="onlyTrue">
    <q-icon
      v-if="value"
      :color="onlyTrueGreen ? trueColour : falseColour"
      :name="trueIcon"
      :size="size"
    />
  </div>
  <div v-else>
    <q-icon
      :color="value ? trueColour : falseColour"
      :name="value ? trueIcon : falseIcon"
      :size="size"
    />
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "BooleanValue",
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
      default: false,
    },
    size: {
      type: String,
      required: false,
      default: "xs",
    },
  },
});
</script>
