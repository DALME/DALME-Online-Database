<template>
  <q-select
    multiple
    clearable
    use-chips
    hide-bottom-space
    input-debounce="350"
    popup-content-class="selectfield"
    :use-input="filterable"
    :error="error"
    :model-value="modelValue"
    :options="options"
    :option-value="(option) => option"
    :option-label="(option) => option.label"
    :popup-content-style="{ zIndex: '9999 !important' }"
    @filter="handleOptions"
    @update:modelValue="onUpdate"
  >
    <q-tooltip v-if="description" class="bg-blue z-max">
      {{ description }}
    </q-tooltip>

    <template v-slot:option="scope">
      <q-item v-bind="scope.itemProps">
        <q-item-section>
          <q-item-label class="text-uppercase text-weight-medium">
            {{ scope.opt.label }}
          </q-item-label>
          <q-item-label
            v-if="scope.opt.caption"
            v-html="scope.opt.caption"
            caption
          >
          </q-item-label>
        </q-item-section>
      </q-item>
    </template>

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
  name: "MultipleSelectField",
  emits: ["update:modelValue"],
  props: {
    modelValue: {
      type: Array,
      default: () => [],
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
    optionsSchema: {
      type: Object,
      required: true,
    },
  },
  setup(props, context) {
    const options = ref(null);

    const error = computed(
      () => !isEmpty(props.validation) && props.validation.errors.length > 0,
    );
    const onUpdate = (value) => context.emit("update:modelValue", value);

    const handleOptions = async (val, update) => {
      // TODO: Depending on whether or not FormVueLate is controlling the field,
      // the callback passed to getOptions might or might not be already
      // resolved at render-time. This isn't ideal, but punting for now.
      const getOptionsPromise = () => {
        try {
          return props.getOptions();
        } catch (e) {
          return props.getOptions;
        }
      };

      // TODO: Regulate when this is called (see attributes),
      await getOptionsPromise().then(async (data) => {
        await props.optionsSchema
          .validate(data, { stripUnknown: true })
          .then((value) => update(() => (options.value = value)));
      });

      update(() => {
        const search = val.toLowerCase();
        options.value = options.value.filter((option) => {
          return (
            !isNil(option.label) &&
            option.label.toLowerCase().indexOf(search) > -1
          );
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

<style lang="scss">
.q-menu.selectfield {
  width: min-content;
}
</style>
