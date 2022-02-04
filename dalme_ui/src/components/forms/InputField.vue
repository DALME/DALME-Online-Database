<template>
  <q-input
    clearable
    hide-bottom-space
    debounce="500"
    :error="error"
    :model-value="modelValue"
    @update:modelValue="onUpdate"
  >
    <template v-slot:error>
      <div>{{ validation.errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { isEmpty } from "ramda";
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "InputField",
  emits: ["update:modelValue"],
  props: {
    modelValue: {
      type: String,
      default: () => "",
    },
    validation: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props, context) {
    const error = computed(
      () => !isEmpty(props.validation) && props.validation.errors.length > 0,
    );
    const onUpdate = (value) => context.emit("update:modelValue", value);

    return { error, onUpdate };
  },
});
</script>
