<template>
  <q-input
    :error="error"
    :model-value="modelValue"
    @blur="onBlur"
    @update:modelValue="onUpdate"
    autogrow
  >
    <template v-slot:error>
      <div>{{ validation.errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "TextField",
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
      () => props.validation.meta.touched && props.validation.errors.length > 0,
    );
    const onBlur = () => props.validation.setTouched(true);
    const onUpdate = (value) => context.emit("update:modelValue", value);

    return { error, onBlur, onUpdate };
  },
});
</script>
