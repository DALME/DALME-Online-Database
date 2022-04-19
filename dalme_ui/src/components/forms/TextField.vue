<template>
  <q-input
    autogrow
    clearable
    debounce="500"
    type="textfield"
    v-model="value"
    :error="errorMessage && meta.touched"
    @blur="handleBlur"
  >
    <Tooltip v-if="description">
      {{ description }}
    </Tooltip>

    <template v-slot:error>
      <div>{{ errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineAsyncComponent, defineComponent } from "vue";

export default defineComponent({
  name: "TextField",
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
    const { errorMessage, handleBlur, meta, value } = useField(
      props.field,
      props.validation,
    );

    return { errorMessage, handleBlur, meta, value };
  },
});
</script>
