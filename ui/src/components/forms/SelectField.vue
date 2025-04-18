<template>
  <q-select
    v-model="value"
    @blur="handleBlur"
    @filter="handleOptions"
    :error="errorMessage && meta.touched"
    :options="options"
    :popup-content-style="{ zIndex: '9999 !important' }"
    :use-input="filterable"
    input-debounce="500"
    popup-content-class="selectfield"
    clearable
  >
    <ToolTip v-if="description">
      {{ description }}
    </ToolTip>

    <template #option="scope">
      <q-item v-bind="scope.itemProps">
        <q-item-section>
          <q-item-label class="text-weight-medium">
            {{ scope.opt.label }}
          </q-item-label>
          <q-item-label v-if="scope.opt.caption" caption>
            {{ scope.opt.caption }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </template>

    <template #no-option>
      <q-item>
        <q-item-section class="text-grey"> No choices </q-item-section>
      </q-item>
    </template>

    <template #error>
      <div>{{ errorMessage }}</div>
    </template>
  </q-select>
</template>

<script>
import { isNil } from "ramda";
import { useField } from "vee-validate";
import { defineAsyncComponent, defineComponent, ref } from "vue";

export default defineComponent({
  name: "SelectField",
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
    filterable: {
      type: Boolean,
      default: true,
    },
    getOptions: {
      type: [Function, Promise],
      required: true,
    },
    optionsSchema: {
      type: Object,
      required: true,
    },
  },

  setup(props) {
    const options = ref(null);

    const { errorMessage, handleBlur, meta, value } = useField(props.field, props.validation);

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

      await getOptionsPromise().then(async (data) => {
        await props.optionsSchema
          .validate(data, { stripUnknown: true })
          .then((value) => update(() => (options.value = value)));
      });

      update(() => {
        const search = val.toLowerCase();
        options.value = Object.freeze(
          options.value.filter((option) => {
            return (
              (!isNil(option.label) &&
                option.label.toString().toLowerCase().indexOf(search) > -1) ||
              (!isNil(option.caption) &&
                option.caption.toString().toLowerCase().indexOf(search) > -1)
            );
          }),
        );
      });
    };

    return {
      errorMessage,
      handleBlur,
      handleOptions,
      meta,
      options,
      value,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-menu.selectfield {
  width: min-content;
}
</style>
