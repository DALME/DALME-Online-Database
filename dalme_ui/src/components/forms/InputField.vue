<template>
  <q-input
    clearable
    hide-bottom-space
    debounce="500"
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
  setup(props) {
    const { errorMessage, handleBlur, meta, value } = useField(
      props.field,
      props.validation,
    );

    return { errorMessage, handleBlur, meta, value };
  },
});
</script>
