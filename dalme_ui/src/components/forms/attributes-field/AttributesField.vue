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
        @click.stop="handleAddField"
      >
        <q-tooltip class="bg-blue z-max"> Add an attribute </q-tooltip>
      </q-btn>

      <q-btn
        round
        class="q-ml-sm"
        size="xs"
        :icon="showing ? 'visibility_off' : 'visibility'"
        @click.stop="showing = !showing"
      >
        <q-tooltip class="bg-blue z-max">
          {{ showing ? "Hide attributes" : "Show attributes" }}
        </q-tooltip>
      </q-btn>
    </div>

    <template v-for="(data, idx) in modelValue" :key="idx">
      <div class="row q-mb-sm" v-show="showing">
        <div class="col-6 q-pr-sm">
          <q-select
            map-options
            label="Attribute"
            class="attribute-select"
            :disable="isRequiredAttribute(data.attribute)"
            :clearable="!isRequiredAttribute(data.attribute)"
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
            @update:modelValue="(option) => handleUpdateAttribute(option, idx)"
          >
            <q-tooltip
              v-if="data.attribute && data.attribute.description"
              class="bg-blue z-max"
              max-width="12rem"
            >
              {{ data.attribute.description }}
            </q-tooltip>
          </q-select>
        </div>

        <div class="q-pl-sm col">
          <template v-if="!data.attribute">
            <q-input disable label="Choose an attribute" />
          </template>
          <template v-else>
            <template v-if="data.attribute.dataType === 'Boolean'">
              <BooleanField
                :field="`attributes[${idx}]`"
                :label="data.attribute.dataType"
                :model-value="data.value"
                :validation="validators[data.attribute.shortName]"
                @update:modelValue="(value) => handleUpdateField(value, idx)"
              />
            </template>
            <template v-else-if="data.attribute.dataType === 'Decimal'">
              <DecimalField
                :field="`attributes[${idx}]`"
                :label="data.attribute.dataType"
                :model-value="data.value"
                :validation="validators[data.attribute.shortName]"
                @update:modelValue="(value) => handleUpdateField(value, idx)"
              />
            </template>
            <template v-else-if="data.attribute.dataType === 'Number'">
              <NumberField
                :field="`attributes[${idx}]`"
                :label="data.attribute.dataType"
                :model-value="data.value"
                :validation="validators[data.attribute.shortName]"
                @update:modelValue="(value) => handleUpdateField(value, idx)"
              />
            </template>
            <template v-else-if="data.attribute.dataType === 'Date'">
              <DateField
                :field="`attributes[${idx}]`"
                :label="data.attribute.dataType"
                :model-value="data.value"
                :validation="validators[data.attribute.shortName]"
                @update:modelValue="(value) => handleUpdateField(value, idx)"
              />
            </template>
            <template v-else-if="data.attribute.dataType === 'Text'">
              <TextField
                :field="`attributes[${idx}]`"
                :label="data.attribute.dataType"
                :model-value="data.value"
                :validation="validators[data.attribute.shortName]"
                @update:modelValue="(value) => handleUpdateField(value, idx)"
              />
            </template>
            <template v-else-if="data.attribute.dataType === 'Options'">
              <SelectField
                v-if="!getOptionsData(data.attribute.shortName).multiple"
                :field="`attributes[${idx}]`"
                :label="data.attribute.dataType"
                :model-value="data.value"
                :filterable="
                  getOptionsData(data.attribute.shortName).filterable
                "
                :getOptions="
                  wrapRequest(getOptionsData(data.attribute.shortName).request)
                "
                :optionsSchema="getOptionsData(data.attribute.shortName).schema"
                :validation="validators[data.attribute.shortName]"
                @update:modelValue="(value) => handleUpdateField(value, idx)"
              />
              <MultipleSelectField
                v-else
                :field="`attributes[${idx}]`"
                :label="data.attribute.dataType"
                :model-value="data.value"
                :filterable="
                  getOptionsData(data.attribute.shortName).filterable
                "
                :getOptions="
                  wrapRequest(getOptionsData(data.attribute.shortName).request)
                "
                :optionsSchema="getOptionsData(data.attribute.shortName).schema"
                :validation="validators[data.attribute.shortName]"
                @update:modelValue="(value) => handleUpdateField(value, idx)"
              />
            </template>
            <template v-else>
              <InputField
                :field="`attributes[${idx}]`"
                :label="data.attribute.dataType"
                :model-value="data.value"
                :validation="validators[data.attribute.shortName]"
                @update:modelValue="(value) => handleUpdateField(value, idx)"
              />
            </template>
          </template>
        </div>

        <div v-if="modelValue.length > 1" class="row items-center">
          <q-btn
            class="q-ml-auto"
            flat
            round
            unelevated
            size="xs"
            icon="clear"
            :text-color="isRequiredAttribute(data.attribute) ? 'grey' : 'black'"
            :disable="isRequiredAttribute(data.attribute)"
            @click.stop="handleRemoveField(idx)"
          >
            <q-tooltip
              v-if="isRequiredAttribute(data.attribute)"
              class="bg-blue z-max"
            >
              Can't delete a required attribute
            </q-tooltip>
          </q-btn>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { isNil, map as rMap } from "ramda";
import { useFieldArray } from "vee-validate";
import { computed, defineComponent, onMounted, ref } from "vue";
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

export default defineComponent({
  name: "AttributesField",
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    required: {
      type: Array,
      default: () => [],
    },
    validators: {
      type: Object,
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
  },
  setup(props, context) {
    const empty = () => ({ attribute: null, value: null });

    const { push, remove, replace } = useFieldArray("attributes");

    const showing = ref(true);
    const options = ref(null);
    const optionCount = ref(null);
    const loading = ref(false);

    const activeAttributes = computed(() =>
      rMap(
        (field) => (field.attribute ? field.attribute.id : null),
        props.modelValue,
      ),
    );

    const isRequiredAttribute = (attribute) =>
      !isNil(attribute) && props.required.includes(attribute.shortName);

    const getOptionsData = (shortName) => attributeFields[shortName].options;

    const wrapRequest = (request) =>
      request
        ? () => fetcher(request()).then((response) => response.json())
        : null;

    const handleAddField = () => {
      const newValue = props.modelValue.slice(0);
      context.emit("update:modelValue", [...newValue, empty()]);
      context.emit("change");
      push(empty());
    };
    const handleUpdateField = (value, idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx].value = !isNil(value) ? value : null;
      context.emit("update:modelValue", newValue);
      context.emit("change");
    };
    const handleRemoveField = (idx) => {
      const newValue = props.modelValue.slice(0);
      newValue.splice(idx, 1);
      context.emit("update:modelValue", newValue);
      context.emit("change");
      remove(idx);
    };
    const handleClearAttribute = (idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx] = empty();
      context.emit("update:modelValue", newValue);
      context.emit("change");
    };
    const handleUpdateAttribute = (option, idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx].attribute = option ? option : null;
      newValue[idx].value = null;
      context.emit("update:modelValue", newValue);
      context.emit("change");
    };

    const handleOptions = async (val, update) => {
      if (isNil(options.value) || options.value.length !== optionCount.value) {
        const { success, data, fetchAPI } = useAPI(context);
        const request = requests.attributeTypes.getAttributeTypes();
        await fetchAPI(request);
        if (success.value)
          await attributeTypesSchema
            .validate(data.value, { stripUnknown: true })
            .then((value) =>
              update(() => {
                options.value = Object.freeze(
                  value.filter(
                    (option) => !activeAttributes.value.includes(option.id),
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
              label.toLowerCase().indexOf(search) > -1 &&
              !activeAttributes.value.includes(option.id)
            );
          }),
        );
      });
    };

    const initAttributes = async () => {
      if (props.required.length === 0) {
        showing.value = false;
        context.emit("update:modelValue", [empty()]);
      } else {
        loading.value = true;
        const { success, data, fetchAPI } = useAPI(context);
        const request = requests.attributeTypes.getAttributeTypesByShortName(
          props.required.join(),
        );
        await fetchAPI(request);
        if (success.value)
          await attributeTypesSchema
            .validate(data.value, { stripUnknown: true })
            .then((value) => {
              let newValue = props.modelValue.slice(0);
              const initial = new Set(
                rMap((field) => field.attribute, newValue),
              );
              for (let attribute of value) {
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
            });
      }
    };

    onMounted(async () => await initAttributes());

    return {
      empty,
      getOptionsData,
      handleAddField,
      handleClearAttribute,
      handleOptions,
      handleRemoveField,
      handleUpdateAttribute,
      handleUpdateField,
      isRequiredAttribute,
      loading,
      options,
      showing,
      wrapRequest,
      yString,
    };
  },
});
</script>

<style lang="scss">
.separator {
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  padding-bottom: 0.5rem;
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
</style>
