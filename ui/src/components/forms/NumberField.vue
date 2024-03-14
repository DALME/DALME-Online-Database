<template>
  <q-input
    clearable
    debounce="500"
    fill-mask="0"
    v-model="value"
    :error="errorMessage && meta.touched"
    @blur="handleBlur"
  >
    <TooltipWidget v-if="description">
      {{ description }}
    </TooltipWidget>

    <template v-slot:error>
      <div>{{ errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineComponent, defineAsyncComponent } from "vue";

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
  components: {
    TooltipWidget: defineAsyncComponent(() => import("@/components/widgets/TooltipWidget.vue")),
  },
  setup(props) {
    const { errorMessage, meta, handleBlur, value } = useField(props.field, props.validation);

    return { errorMessage, meta, handleBlur, value };
  },
});
</script>
