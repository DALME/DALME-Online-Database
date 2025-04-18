<template>
  <q-input
    @blur="handleBlur"
    @update:model-value="onUpdate"
    :error="errorMessage && meta.touched"
    :model-value="modelValue"
    label="Date (YYYY-MM-DD)"
    mask="####-##-##"
  >
    <ToolTip v-if="description">
      {{ description }}
    </ToolTip>

    <template #error>
      <div>{{ errorMessage }}</div>
    </template>

    <template #append>
      <q-icon class="cursor-pointer" name="event">
        <q-popup-proxy
          ref="qDateProxy"
          class="z-max"
          transition-hide="scale"
          transition-show="scale"
          cover
        >
          <q-date @update:model-value="onUpdate" :model-value="modelValue" mask="YYYY-MM-DD">
            <div class="row items-center justify-end">
              <q-btn v-close-popup color="primary" label="Close" flat />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineAsyncComponent, defineComponent } from "vue";

export default defineComponent({
  name: "DateField",
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
    modelValue: {
      type: String,
      default: () => "",
    },
  },
  emits: ["update:modelValue"],
  setup(props, context) {
    const { errorMessage, meta, handleBlur } = useField(props.field, props.validation);

    const onUpdate = (value) => {
      context.emit("update:modelValue", value);
    };

    return { errorMessage, meta, onUpdate, handleBlur };
  },
});
</script>
