<template>
  <q-select
    clearable
    hide-bottom-space
    input-debounce="350"
    :use-input="filterable"
    :error="error"
    :model-value="modelValue"
    :options="options"
    :option-label="optionLabel"
    :option-value="(option) => option"
    :popup-content-style="{ zIndex: '9999 !important' }"
    @filter="handleOptions"
    @update:modelValue="onUpdate"
  >
    <q-tooltip v-if="description" class="bg-blue z-max">
      {{ description }}
    </q-tooltip>

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
import { isEmpty, isNil } from "ramda";
import { computed, defineComponent, ref } from "vue";

export default defineComponent({
  name: "SelectField",
  emits: ["update:modelValue"],
  props: {
    modelValue: {
      type: Object,
    },
    validation: {
      type: Object,
      default: () => ({}),
    },
    description: {
      type: [Boolean, String],
      default: () => false,
    },
    filterable: {
      type: Boolean,
      default: false,
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

    const error = computed(
      () => !isEmpty(props.validation) && props.validation.errors.length > 0,
    );
    const onUpdate = (value) => context.emit("update:modelValue", value);

    const handleOptions = async (val, update) => {
      const data = await props.getOptions();
      await props.optionsSchema
        .validate(data, { stripUnknown: true })
        .then((value) => update(() => (options.value = value)));

      update(() => {
        const search = val.toLowerCase();
        options.value = options.value.filter((option) => {
          const getLabel = () => {
            try {
              return props.optionLabel(option);
            } catch (_) {
              return option[props.optionLabel];
            }
          };
          const label = getLabel();
          return !isNil(label) && label.toLowerCase().indexOf(search) > -1;
        });
      });
    };

    return {
      handleOptions,
      error,
      onUpdate,
      options,
    };
  },
});
</script>
