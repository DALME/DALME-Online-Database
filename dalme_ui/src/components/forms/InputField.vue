<template>
  <q-input
    clearable
    debounce="500"
    v-model="value"
    :error="errorMessage && meta.touched"
    @blur="handleBlur"
  >
    <TooltipWidget v-if="description">
      {{ description }}
    </TooltipWidget>

    <template v-slot:error>
      <span>{{ errorMessage }}</span>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineComponent, defineAsyncComponent } from "vue";

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
    TooltipWidget: defineAsyncComponent(() =>
      import("@/components/widgets/TooltipWidget.vue"),
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
