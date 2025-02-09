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
    <ToolTip v-if="description">
      {{ description }}
    </ToolTip>

    <template v-slot:error>
      <div>{{ errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineComponent, defineAsyncComponent } from "vue";

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
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
  },
  setup(props) {
    const { errorMessage, handleBlur, meta, value } = useField(props.field, props.validation);

    return { errorMessage, handleBlur, meta, value };
  },
});
</script>
