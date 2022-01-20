<template>
  <q-input
    :model-value="modelValue"
    :error="error"
    @update:modelValue="onUpdate"
    mask="date"
  >
    <template v-slot:append>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy
          ref="qDateProxy"
          cover
          transition-show="scale"
          transition-hide="scale"
          class="z-max"
        >
          <q-date :model-value="modelValue" @update:modelValue="onUpdate">
            <div class="row items-center justify-end">
              <q-btn v-close-popup label="Close" color="primary" flat />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>

    <template v-slot:error>
      <div>{{ validation.errorMessage }}</div>
    </template>
  </q-input>
</template>

<script>
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "InputField",
  props: {
    modelValue: {
      type: String,
      default: () => "",
    },
    validation: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props, context) {
    const error = computed(() => props.validation.errors.length > 0);
    const onUpdate = (value) => context.emit("update:modelValue", value);

    return { error, onUpdate };
  },
});
</script>
