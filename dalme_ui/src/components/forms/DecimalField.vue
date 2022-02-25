<template>
  <q-input
    clearable
    reverse-fill-mask
    debounce="500"
    mask="#.##"
    fill-mask="0"
    v-model="value"
    :error="errorMessage && meta.touched"
    @blur="handleBlur"
  >
    <q-tooltip v-if="description" class="bg-blue z-max">
      {{ description }}
    </q-tooltip>

    <template v-slot:error>
      <span>{{ errorMessage }}</span>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineComponent } from "vue";

export default defineComponent({
  name: "DecimalField",
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
    const { errorMessage, meta, handleBlur, value } = useField(
      props.field,
      props.validation,
    );

    return { errorMessage, meta, handleBlur, value };
  },
});
</script>
