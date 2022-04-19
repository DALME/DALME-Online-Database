<template>
  <q-input
    clearable
    debounce="500"
    v-model="value"
    :error="errorMessage && meta.touched"
    @blur="handleBlur"
  >
    <Tooltip v-if="description">
      {{ description }}
    </Tooltip>

    <template v-slot:error>
      <span>{{ errorMessage }}</span>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineAsyncComponent, defineComponent } from "vue";

export default defineComponent({
  name: "InputField",
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
  components: {
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  setup(props) {
    const { errorMessage, handleBlur, meta, value } = useField(
      props.field,
      props.validation,
    );

    return { errorMessage, handleBlur, meta, value };
  },
});
</script>
