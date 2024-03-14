<template>
  <q-input
    label="Date (YYYY-MM-DD)"
    mask="####-##-##"
    :model-value="modelValue"
    :error="errorMessage && meta.touched"
    @blur="handleBlur"
    @update:modelValue="onUpdate"
  >
    <TooltipWidget v-if="description">
      {{ description }}
    </TooltipWidget>

    <template v-slot:error>
      <div>{{ errorMessage }}</div>
    </template>

    <template v-slot:append>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy
          ref="qDateProxy"
          cover
          transition-show="scale"
          transition-hide="scale"
          class="z-max"
        >
          <q-date mask="YYYY-MM-DD" :model-value="modelValue" @update:modelValue="onUpdate">
            <div class="row items-center justify-end">
              <q-btn v-close-popup label="Close" color="primary" flat />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script>
import { useField } from "vee-validate";
import { defineComponent, defineAsyncComponent } from "vue";

export default defineComponent({
  name: "DateField",
  components: {
    TooltipWidget: defineAsyncComponent(() => import("@/components/widgets/TooltipWidget.vue")),
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
  setup(props, context) {
    const { errorMessage, meta, handleBlur } = useField(props.field, props.validation);

    const onUpdate = (value) => {
      context.emit("update:modelValue", value);
    };

    return { errorMessage, meta, onUpdate, handleBlur };
  },
});
</script>
