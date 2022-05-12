<template>
  <div class="attributes-field column q-my-sm" :class="{ separator: !showing }">
    <div class="row items-center q-my-sm">
      <div class="q-field__label no-pointer-events q-mr-auto">
        {{
          !showing && modelValue !== [empty()]
            ? `Attributes (${modelValue.length})`
            : "Attributes"
        }}
      </div>

      <q-spinner v-if="loading" color="primary" size="xs" />
      <q-btn
        round
        class="q-ml-sm"
        color="amber"
        icon="add"
        size="xs"
        text-color="black"
        v-show="showing"
        :disable="modelValue.length === allowed.length"
        @click.stop="handleAddField"
      >
        <Tooltip> Add an attribute </Tooltip>
      </q-btn>

      <q-btn
        round
        class="q-ml-sm"
        size="xs"
        :icon="showing ? 'visibility_off' : 'visibility'"
        @click.stop="showing = !showing"
      >
        <Tooltip>
          {{ showing ? "Hide attributes" : "Show attributes" }}
        </Tooltip>
      </q-btn>

      <Tooltip v-if="description">
        {{ description }}
      </Tooltip>
    </div>

    <template v-if="showing">
      <template v-if="modelValue.length > 0">
        <template
          v-for="({ 0: data, 1: field }, idx) in zip(modelValue, fields)"
          :key="`${idx}-${field.key}`"
        >
          <div class="row q-mb-sm" v-show="showing">
            <div class="col-6 q-pr-sm">
              <q-select
                map-options
                label="Attribute"
                class="attribute-select"
                :clearable="!isRequiredAttribute(data.attribute)"
                :disable="isRequiredAttribute(data.attribute)"
                :model-value="data.attribute"
                :options="options"
                :option-label="
                  (option) =>
                    option
                      ? isRequiredAttribute(data.attribute)
                        ? `${option.name} *`
                        : option.name
                      : null
                "
                :option-value="(option) => option"
                :popup-content-style="{ zIndex: '9999 !important' }"
                :use-input="true"
                @clear="() => handleClearAttribute(idx)"
                @filter="handleOptions"
                @update:modelValue="
                  (option) => handleUpdateAttribute(option, idx)
                "
              >
                <Tooltip v-if="data.attribute && data.attribute.description">
                  {{ data.attribute.description }}
                </Tooltip>
              </q-select>
            </div>

            <div class="q-pl-sm col">
              <template v-if="!data.attribute">
                <q-input disable label="Choose an attribute" />
              </template>
              <template v-else>
                <template v-if="data.attribute.dataType === 'Boolean'">
                  <BooleanField
                    v-model="data.value"
                    :field="`attributes[${idx}].value`"
                    :label="data.attribute.dataType"
                    :validation="validators[data.attribute.shortName]"
                  />
                </template>
                <template v-else-if="data.attribute.dataType === 'Decimal'">
                  <DecimalField
                    v-model="data.value"
                    :field="`attributes[${idx}].value`"
                    :label="data.attribute.dataType"
                    :validation="validators[data.attribute.shortName]"
                  />
                </template>
                <template v-else-if="data.attribute.dataType === 'Number'">
                  <NumberField
                    v-model="data.value"
                    :field="`attributes[${idx}].value`"
                    :label="data.attribute.dataType"
                    :validation="validators[data.attribute.shortName]"
                  />
                </template>
                <template v-else-if="data.attribute.dataType === 'Date'">
                  <DateField
                    v-model="data.value"
                    :field="`attributes[${idx}].value`"
                    :label="data.attribute.dataType"
                    :validation="validators[data.attribute.shortName]"
                  />
                </template>
                <template v-else-if="data.attribute.dataType === 'Text'">
                  <TextField
                    v-model="data.value"
                    :field="`attributes[${idx}].value`"
                    :label="data.attribute.dataType"
                    :validation="validators[data.attribute.shortName]"
                  />
                </template>
                <template v-else-if="data.attribute.dataType === 'Options'">
                  <SelectField
                    v-if="!getOptionsData(data.attribute.shortName).multiple"
                    v-model="data.value"
                    :field="`attributes[${idx}].value`"
                    :label="data.attribute.dataType"
                    :filterable="
                      getOptionsData(data.attribute.shortName).filterable
                    "
                    :getOptions="
                      wrapRequest(
                        getOptionsData(data.attribute.shortName).request,
                      )
                    "
                    :optionsSchema="
                      getOptionsData(data.attribute.shortName).schema
                    "
                    :validation="validators[data.attribute.shortName]"
                  />
                  <MultipleSelectField
                    v-else
                    v-model="data.value"
                    :field="`attributes[${idx}].value`"
                    :label="data.attribute.dataType"
                    :filterable="
                      getOptionsData(data.attribute.shortName).filterable
                    "
                    :getOptions="
                      wrapRequest(
                        getOptionsData(data.attribute.shortName).request,
                      )
                    "
                    :optionsSchema="
                      getOptionsData(data.attribute.shortName).schema
                    "
                    :validation="validators[data.attribute.shortName]"
                  />
                </template>
                <template v-else>
                  <InputField
                    v-model="data.value"
                    :field="`attributes[${idx}].value`"
                    :label="data.attribute.dataType"
                    :validation="validators[data.attribute.shortName]"
                  />
                </template>
              </template>
            </div>

            <div
              v-if="!required || modelValue.length > 1"
              class="row items-center"
            >
              <q-btn
                class="q-ml-auto"
                flat
                round
                unelevated
                size="xs"
                icon="clear"
                :text-color="
                  isRequiredAttribute(data.attribute) ? 'grey' : 'black'
                "
                :disable="isRequiredAttribute(data.attribute)"
                @click.stop="handleRemoveField(idx)"
              >
                <Tooltip v-if="isRequiredAttribute(data.attribute)">
                  Can't delete a required attribute
                </Tooltip>
              </q-btn>
            </div>
          </div>
        </template>
      </template>
      <template v-else>
        <div class="text-subtitle1 placeholder">
          <p>No attributes defined.</p>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import { isNil, filter as rFilter, map as rMap, zip } from "ramda";
import { useFieldArray } from "vee-validate";
import {
  computed,
  defineAsyncComponent,
  defineComponent,
  onMounted,
  ref,
  unref,
} from "vue";
import { string as yString } from "yup";

import { fetcher, requests } from "@/api";
import {
  BooleanField,
  DateField,
  DecimalField,
  InputField,
  MultipleSelectField,
  NumberField,
  SelectField,
  TextField,
} from "@/components/forms";
import { attributeTypesSchema } from "@/schemas";
import { useAPI } from "@/use";

import { attributeFields } from "./attributes";
import { empty } from "./normalize";

export default defineComponent({
  name: "AttributesField",
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    description: {
      type: [Boolean, String],
      default: () => false,
    },
    allowed: {
      type: Array,
      default: () => [],
    },
    required: {
      type: Array,
      default: () => [],
    },
    validators: {
      required: true,
    },
  },
  components: {
    BooleanField,
    DateField,
    DecimalField,
    InputField,
    MultipleSelectField,
    NumberField,
    SelectField,
    TextField,
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  setup(props, context) {
    const { apiInterface } = useAPI();
    const { fields, push, replace, remove } = useFieldArray("attributes");

    const loading = ref(false);
    const showing = ref(false);
    const options = ref(null);
    const optionCount = ref(null);

    const activeAttributes = computed(() =>
      rMap(
        (field) => (field.attribute ? field.attribute.id : null),
        props.modelValue,
      ),
    );

    const isRequiredAttribute = (attribute) =>
      !isNil(attribute) &&
      props.required &&
      props.required.includes(attribute.shortName);

    const getOptionsData = (shortName) => attributeFields[shortName].options;

    const wrapRequest = (request) =>
      request
        ? () => fetcher(request()).then((response) => response.json())
        : null;

    const handleAddField = () => {
      const newValue = [...unref(props.modelValue), empty()];
      push(empty());
      context.emit("update:modelValue", newValue);
    };
    const handleRemoveField = (idx) => {
      const newValue = unref(props.modelValue);
      newValue.splice(idx, 1);
      remove(idx);
      context.emit("update:modelValue", newValue);
    };
    const handleClearAttribute = (idx) => {
      const newValue = unref(props.modelValue);
      newValue[idx] = empty();
      context.emit("update:modelValue", newValue);
    };
    const handleUpdateAttribute = (option, idx) => {
      const newValue = unref(props.modelValue);
      newValue[idx].attribute = option ? option : null;
      newValue[idx].value = null;
      context.emit("update:modelValue", newValue);
    };

    const handleOptions = async (val, update) => {
      if (isNil(options.value) || options.value.length !== optionCount.value) {
        const { success, data, fetchAPI } = apiInterface();
        const request = requests.attributeTypes.getAttributeTypes();
        await fetchAPI(request);
        if (success.value)
          await attributeTypesSchema
            .validate(data.value, { stripUnknown: true })
            .then((value) =>
              update(() => {
                options.value = Object.freeze(
                  value.filter(
                    (option) =>
                      props.allowed.includes(option.shortName) &&
                      !activeAttributes.value.includes(option.id),
                  ),
                );
                optionCount.value = value.length;
              }),
            );
      }

      update(() => {
        const search = val.toLowerCase();
        options.value = Object.freeze(
          options.value.filter((option) => {
            const label = option.name;
            return (
              !isNil(label) &&
              label.toString().toLowerCase().indexOf(search) > -1 &&
              !activeAttributes.value.includes(option.id)
            );
          }),
        );
      });
    };

    const initAttributes = async () => {
      if (props.modelValue.length > 0) {
        // Filter out any non-permitted attributes from editing before sorting.
        const newValue = rFilter(
          ({ attribute }) => props.allowed.includes(attribute.shortName),
          unref(props.modelValue),
        ).sort(
          (x, y) =>
            isRequiredAttribute(y.attribute) - isRequiredAttribute(x.attribute),
        );
        replace(newValue);
        context.emit("update:modelValue", newValue);
      } else {
        if (props.required) {
          loading.value = true;
          const { success, data, fetchAPI } = apiInterface();
          const request = requests.attributeTypes.getAttributeTypesByShortName(
            props.required.join(),
          );
          await fetchAPI(request);
          if (success.value)
            await attributeTypesSchema
              .validate(data.value, { stripUnknown: true })
              .then((value) => {
                let newValue = unref(props.modelValue);
                const initial = new Set(
                  rMap((field) => field.attribute, newValue),
                );
                for (const attribute of value) {
                  if (
                    !activeAttributes.value.includes(attribute.id) &&
                    !initial.has(attribute.shortName)
                  ) {
                    newValue = [{ attribute, value: null }, ...newValue];
                  }
                }
                replace(newValue);
                context.emit("update:modelValue", newValue);
                loading.value = false;
                showing.value = true;
              });
        }
      }
    };

    onMounted(async () => await initAttributes());

    return {
      empty,
      fields,
      getOptionsData,
      handleAddField,
      handleClearAttribute,
      handleOptions,
      handleRemoveField,
      handleUpdateAttribute,
      isRequiredAttribute,
      loading,
      options,
      showing,
      wrapRequest,
      yString,
      zip,
    };
  },
});
</script>

<style lang="scss">
.attributes-field {
  will-transform: auto;
}
.attributes-field .q-field__after,
.attributes-field .q-field__append {
  padding-left: 0 !important;
}
.attributes-field .q-field--with-bottom {
  padding-bottom: 0;
}
.attribute-select .q-field__native {
  color: black;
}
div.q-field__bottom {
  margin-bottom: 5px;
}
.placeholder {
  align-items: center;
  border-bottom: 1px solid #c2c2c2;
  color: rgba(0, 0, 0, 0.6);
  font-weight: 400;
  line-height: 18px;
  margin-bottom: 8px;
  padding-bottom: 17px;
  padding-top: 20px;
}
.placeholder > p {
  margin: 0;
}
.separator {
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  padding-bottom: 0.5rem;
}
</style>
