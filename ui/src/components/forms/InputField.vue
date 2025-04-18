<template>
  <q-input
    v-model="value"
    @blur="handleBlur"
    :error="errorMessage && meta.touched"
    debounce="500"
    clearable
  >
    <ToolTip v-if="description">
      {{ description }}
    </ToolTip>

    <template #error>
      <span>{{ errorMessage }}</span>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineAsyncComponent, defineComponent } from "vue";

export default defineComponent({
  name: "InputField",
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
      required: true,
    },
    description: {
      type: [Boolean, String],
      default: () => false,
    },
  },

  setup(props) {
    const { errorMessage, handleBlur, meta, value } = useField(props.field, props.validation);

    return { errorMessage, handleBlur, meta, value };
  },
});
</script>
