<template>
  <q-select
    v-model="value"
    @blur="handleBlur"
    :error="errorMessage && meta.touched"
    :options="options"
    :popup-content-style="{ zIndex: '9999 !important' }"
    input-debounce="350"
    label="True or False"
    clearable
  >
    <ToolTip v-if="description">
      {{ description }}
    </ToolTip>

    <template #error>
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
  components: {
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
  },
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

    const { errorMessage, meta, handleBlur, value } = useField(props.field, props.validation);

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
