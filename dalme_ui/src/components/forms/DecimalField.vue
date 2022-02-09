<template>
  <q-input
    clearable
    hide-bottom-space
    reverse-fill-mask
    debounce="500"
    mask="#.##"
    fill-mask="0"
    :error="error"
    :model-value="modelValue"
    @update:modelValue="onUpdate"
  >
    <q-tooltip v-if="description" class="bg-blue z-max">
      {{ description }}
    </q-tooltip>

    <template v-slot:error>
      <div>{{ validation.errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { isEmpty } from "ramda";
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "DecimalField",
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
    description: {
      type: [Boolean, String],
      default: () => false,
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
