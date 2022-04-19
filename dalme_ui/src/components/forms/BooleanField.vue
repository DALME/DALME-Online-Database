<template>
  <q-select
    clearable
    input-debounce="350"
    label="True or False"
    v-model="value"
    :error="errorMessage && meta.touched"
    :options="options"
    :popup-content-style="{ zIndex: '9999 !important' }"
    @blur="handleBlur"
  >
    <Tooltip v-if="description">
      {{ description }}
    </Tooltip>

    <template v-slot:error>
      <div>{{ errorMessage }}</div>
    </template>
  </q-select>
</template>

<script>
import { useField } from "vee-validate";
import { defineAsyncComponent, defineComponent } from "vue";

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
  components: {
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
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
