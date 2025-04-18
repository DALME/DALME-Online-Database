<template>
  <q-input
    v-model="value"
    @blur="handleBlur"
    :error="errorMessage && meta.touched"
    debounce="500"
    type="textfield"
    autogrow
    clearable
  >
    <ToolTip v-if="description">
      {{ description }}
    </ToolTip>

    <template #error>
      <div>{{ errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineAsyncComponent, defineComponent } from "vue";

export default defineComponent({
  name: "TextField",
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
    const { errorMessage, handleBlur, meta, value } = useField(props.field, props.validation);

    return { errorMessage, handleBlur, meta, value };
  },
});
</script>
