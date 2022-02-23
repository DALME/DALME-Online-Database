<template>
  <q-select
    multiple
    clearable
    use-chips
    hide-bottom-space
    input-debounce="350"
    popup-content-class="selectfield"
    v-model="value"
    :error="errorMessage && meta.touched"
    :options="options"
    :option-label="(option) => option.label"
    :popup-content-style="{ zIndex: '9999 !important' }"
    :use-input="filterable"
    @blur="handleBlur"
    @filter="handleOptions"
  >
    <q-tooltip v-if="description" class="bg-blue z-max">
      {{ description }}
    </q-tooltip>

    <template v-slot:option="scope">
      <q-item v-bind="scope.itemProps">
        <q-item-section>
          <q-item-label class="text-weight-medium">
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
      <div>{{ errorMessage }}</div>
    </template>
  </q-select>
</template>

<script>
import { useField } from "vee-validate";
import { isNil } from "ramda";
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "MultipleSelectField",
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
    filterable: {
      type: Boolean,
      default: true,
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
  setup(props) {
    const options = ref(null);

    const { errorMessage, meta, handleBlur, value } = useField(
      props.field,
      props.validation,
    );

    const handleOptions = async (val, update) => {
      // TODO: Depending on whether or not FormVueLate is controlling the field,
      // the fetch callback passed to getOptions might, or might not, be already
      // resolved at render-time. This isn't ideal, but punting for now.
      const getOptionsPromise = () => {
        try {
          return props.getOptions();
        } catch (e) {
          return props.getOptions;
        }
      };

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
      errorMessage,
      handleOptions,
      meta,
      options,
      handleBlur,
      value,
    };
  },
});
</script>

<style lang="scss">
.q-menu.selectfield {
  width: min-content;
}
</style>
