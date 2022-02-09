<template>
  <q-select
    clearable
    hide-bottom-space
    input-debounce="350"
    label="True or False"
    :error="error"
    :model-value="modelValue"
    :options="options"
    :option-value="(option) => option"
    :popup-content-style="{ zIndex: '9999 !important' }"
    @update:modelValue="onUpdate"
  >
    <q-tooltip v-if="description" class="bg-blue z-max">
      {{ description }}
    </q-tooltip>

    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-grey"> No choices </q-item-section>
      </q-item>
    </template>

    <template v-slot:error>
      <div>{{ validation.errorMessage }}</div>
    </template>
  </q-select>
</template>

<script>
import { isEmpty } from "ramda";
import { computed, defineComponent } from "vue";

import { booleanOptions } from "@/forms/constants";

export default defineComponent({
  name: "BooleanField",
  emits: ["update:modelValue"],
  props: {
    modelValue: {
      type: Object,
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
    const options = booleanOptions;

    const error = computed(
      () => !isEmpty(props.validation) && props.validation.errors.length > 0,
    );
    const onUpdate = (value) => context.emit("update:modelValue", value);

    return {
      error,
      onUpdate,
      options,
    };
  },
});
</script>
