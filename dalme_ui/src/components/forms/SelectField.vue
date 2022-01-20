<template>
  <q-select
    use-chips
    hide-bottom-space
    :error="error"
    :model-value="modelValue"
    :options="options"
    :option-label="optionLabel"
    :popup-content-style="{ zIndex: '9999 !important' }"
    @filter="handleOptions"
    @update:modelValue="onUpdate"
  >
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-grey"> No choices </q-item-section>
      </q-item>
    </template>

    <template v-slot:error>
      <div>{{ validation.errorMessage }}</div>
    </template>
  </q-select>
</template>

<script>
import { computed, defineComponent, ref } from "vue";

export default defineComponent({
  name: "SelectField",
  props: {
    modelValue: {
      type: Object,
    },
    validation: {
      type: Object,
      default: () => ({}),
    },
    getOptions: {
      type: Function,
      required: true,
    },
    optionLabel: {
      type: [Function, String],
      required: true,
    },
    optionsSchema: {
      type: Object,
      required: true,
      error: false,
    },
  },
  setup(props, context) {
    const options = ref(null);

    const error = computed(() => props.validation.errors.length > 0);
    const onUpdate = (value) => context.emit("update:modelValue", value);

    const handleOptions = async (val, update) => {
      const data = await props.getOptions();
      await props.optionsSchema
        .validate(data, { stripUnknown: true })
        .then((value) => update(() => (options.value = value)));
    };

    return {
      handleOptions,
      error,
      // onBlur,
      onUpdate,
      options,
    };
  },
});
</script>
