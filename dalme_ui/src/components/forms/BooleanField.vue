<template>
  <q-select
    clearable
    hide-bottom-space
    input-debounce="350"
    label="True or False"
    v-model="value"
    :error="errorMessage && meta.touched"
    :options="options"
    :option-value="(option) => option"
    :popup-content-style="{ zIndex: '9999 !important' }"
    @blur="handleBlur"
  >
    <q-tooltip v-if="description" class="bg-blue z-max">
      {{ description }}
    </q-tooltip>

    <template v-slot:error>
      <div>{{ errorMessage }}</div>
    </template>
  </q-select>
</template>

<script>
import { useField } from "vee-validate";
import { defineComponent } from "vue";

import { booleanOptions } from "@/forms/constants";

export default defineComponent({
  name: "BooleanField",
  props: {
    field: {
      type: String,
      required: true,
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
  setup(props) {
    const options = booleanOptions;

    const { errorMessage, meta, handleBlur, value } = useField(
      props.field,
      props.validation,
    );

    return {
      errorMessage,
      meta,
      options,
      handleBlur,
      value,
    };
  },
});
</script>
