<template>
  <div class="attributes-field column q-my-sm" :class="{ separator: !showing }">
    <div class="row items-center q-my-sm">
      <div class="q-field__label no-pointer-events q-mr-auto q-mr-sm">
        {{
          !showing && modelValue !== [[null, null]]
            ? `Attributes (${modelValue.length})`
            : "Attributes"
        }}
      </div>

      <q-btn
        v-show="showing"
        round
        color="amber"
        text-color="black"
        size="xs"
        icon="add"
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

    <template
      v-for="({ 0: attribute, 1: value }, idx) in modelValue"
      :key="idx"
    >
      <div class="row flex-center" v-show="showing">
        <div class="col-6 q-pr-sm">
          <q-select
            use-input
            emit-value
            hide-bottom-space
            label="Attribute"
            class="attribute-select"
            :disable="isRequiredAttribute(attribute)"
            :clearable="!isRequiredAttribute(attribute)"
            :model-value="attribute"
            :options="options"
            :option-label="
              (option) =>
                option
                  ? isRequiredAttribute(attribute)
                    ? `${option.name} *`
                    : option.name
                  : null
            "
            :option-value="(option) => option"
            :popup-content-style="{ zIndex: '9999 !important' }"
            @clear="() => handleClearAttribute(idx)"
            @filter="handleOptions"
            @update:modelValue="(option) => handleUpdateAttribute(option, idx)"
          >
            <q-tooltip
              v-if="attribute && attribute.description"
              class="bg-blue z-max"
              max-width="12rem"
            >
              {{ attribute.description }}
            </q-tooltip>
          </q-select>
        </div>
        <div class="q-pl-sm col">
          <template v-if="!attribute">
            <q-input disable label="Choose an attribute" />
          </template>
          <template v-else-if="attribute && attribute.dataType === 'Boolean'">
            <BooleanField
              :model-value="value"
              @update:modelValue="(value) => handleUpdateField(value, idx)"
            />
          </template>
          <template v-else-if="attribute && attribute.dataType === 'Decimal'">
            <DecimalField
              :model-value="value"
              @update:modelValue="(value) => handleUpdateField(value, idx)"
            />
          </template>
          <template v-else-if="attribute && attribute.dataType === 'Number'">
            <NumberField
              :model-value="value"
              @update:modelValue="(value) => handleUpdateField(value, idx)"
            />
          </template>
          <template v-else-if="attribute && attribute.dataType === 'Date'">
            <DateField
              :model-value="value"
              @update:modelValue="(value) => handleUpdateField(value, idx)"
            />
          </template>
          <template v-else-if="attribute && attribute.dataType === 'Text'">
            <TextField
              :model-value="value"
              @update:modelValue="(value) => handleUpdateField(value, idx)"
            />
          </template>
          <template v-else-if="attribute && attribute.dataType === 'Options'">
            <SelectField
              :model-value="value"
              @update:modelValue="(value) => handleUpdateField(value, idx)"
            />
          </template>
          <template v-else>
            <InputField
              :model-value="value"
              @update:modelValue="(value) => handleUpdateField(value, idx)"
            />
          </template>
        </div>
        <div class="col-1" v-if="modelValue.length > 1">
          <div class="row">
            <q-btn
              class="q-ml-auto"
              flat
              round
              unelevated
              size="xs"
              icon="clear"
              :text-color="isRequiredAttribute(attribute) ? 'grey' : 'black'"
              :disable="isRequiredAttribute(attribute)"
              @click.stop="handleRemoveField(idx)"
            >
              <q-tooltip
                v-if="isRequiredAttribute(attribute)"
                class="bg-blue z-max"
              >
                Can't delete a required attribute
              </q-tooltip>
            </q-btn>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { isNil, map as rMap } from "ramda";
import { computed, defineComponent, onMounted, ref } from "vue";
import { string as yString } from "yup";

import { requests } from "@/api";
import {
  BooleanField,
  DateField,
  DecimalField,
  InputField,
  NumberField,
  SelectField,
  TextField,
} from "@/components/forms";
import { attributeTypesSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    required: {
      type: Array,
      default: () => [],
    },
  },
  components: {
    BooleanField,
    DateField,
    DecimalField,
    InputField,
    NumberField,
    SelectField,
    TextField,
  },
  setup(props, context) {
    const showing = ref(true);
    const options = ref(null);
    const optionCount = ref(null);

    const activeAttributes = computed(() =>
      rMap((field) => (field[0] ? field[0].id : null), props.modelValue),
    );

    const isRequiredAttribute = (attribute) =>
      !isNil(attribute) && props.required.includes(attribute.shortName);

    const handleAddField = () => {
      context.emit("update:modelValue", [
        ...props.modelValue.slice(0),
        [null, null],
      ]);
    };
    const handleClearAttribute = (idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx] = [null, null];
      context.emit("update:modelValue", newValue);
    };
    const handleUpdateAttribute = (option, idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx][0] = option ? option : null;
      newValue[idx][1] = null;
      context.emit("update:modelValue", newValue);
    };
    const handleUpdateField = (value, idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx][1] = !isNil(value) ? value : null;
      context.emit("update:modelValue", newValue);
    };
    const handleRemoveField = (idx) => {
      const newValue = props.modelValue.slice(0);
      newValue.splice(idx, 1);
      context.emit("update:modelValue", newValue);
    };

    const handleOptions = async (val, update) => {
      if (isNil(options.value) || options.value.length !== optionCount.value) {
        const { success, data, fetchAPI } = useAPI(context);
        const request = requests.attributes.getAttributeTypes();
        await fetchAPI(request);
        if (success.value)
          await attributeTypesSchema
            .validate(data.value, { stripUnknown: true })
            .then((value) =>
              update(() => {
                options.value = Object.freeze(value);
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
        context.emit("update:modelValue", [[null, null]]);
      } else {
        const { success, data, fetchAPI } = useAPI(context);
        const request = requests.attributes.getAttributeTypesByShortName(
          props.required.join(),
        );
        await fetchAPI(request);
        if (success.value)
          await attributeTypesSchema
            .validate(data.value, { stripUnknown: true })
            .then((value) => {
              let newValue = props.modelValue.slice(0);
              const initial = new Set(rMap((field) => field[0], newValue));
              for (let attribute of value) {
                if (
                  !activeAttributes.value.includes(attribute.id) &&
                  !initial.has(attribute.shortName)
                ) {
                  newValue = [[attribute, null], ...newValue];
                }
              }
              context.emit("update:modelValue", newValue);
            });
      }
    };

    onMounted(async () => await initAttributes());

    return {
      handleAddField,
      handleOptions,
      handleRemoveField,
      handleClearAttribute,
      handleUpdateAttribute,
      handleUpdateField,
      isRequiredAttribute,
      options,
      showing,
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
.attribute-select {
}
.attribute-select .q-select__dropdown-icon {
  display: none;
}
.attribute-select .q-field__native {
  color: black;
}
</style>
