<template>
  <div></div>
</template>

<script>
import { defineComponent } from "vue";

// import { SelectField, TextField } from "@/components/forms";

export default defineComponent({
  name: "CreditsField",
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    required: {
      type: Array,
      default: () => [],
    },
    validators: {
      type: Object,
      required: true,
    },
  },
  components: {
    // SelectField,
    // TextField,
  },
  setup(props, context) {
    return {};
  },
});
</script>
