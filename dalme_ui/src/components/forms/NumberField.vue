<template>
  <q-input
    clearable
    hide-bottom-space
    debounce="500"
    fill-mask="0"
    v-model="value"
    :error="errorMessage && meta.touched"
    @blur="handleBlur"
  >
    <q-tooltip v-if="description" class="bg-blue z-max">
      {{ description }}
    </q-tooltip>

    <template v-slot:error>
      <div>{{ errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineComponent } from "vue";

export default defineComponent({
  name: "NumberField",
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
