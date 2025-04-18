<template>
  <div :class="{ separator: !showing }" class="agents-field column q-my-sm">
    <div class="row items-center q-my-sm">
      <div class="q-field__label no-pointer-events q-mr-auto">
        {{
          !showing && !empty(modelValue) ? `Named persons (${modelValue.length})` : "Named persons"
        }}
      </div>

      <q-spinner v-if="loading" color="primary" size="xs" />
      <q-btn
        v-show="showing"
        @click.stop="handleAddField"
        class="q-ml-sm"
        color="amber"
        icon="add"
        size="xs"
        text-color="black"
        round
      >
        <ToolTip> Add a named person </ToolTip>
      </q-btn>

      <q-btn
        @click.stop="showing = !showing"
        :icon="showing ? 'visibility_off' : 'visibility'"
        class="q-ml-sm"
        size="xs"
        round
      >
        <ToolTip>
          {{ showing ? "Hide named persons" : "Show named persons" }}
        </ToolTip>
      </q-btn>

      <ToolTip v-if="description">
        {{ description }}
      </ToolTip>
    </div>

    <template v-if="showing">
      <template v-if="modelValue.length > 0">
        <template v-for="({ 0: data, 1: field }, idx) in zip(modelValue, fields)" :key="field.key">
          <div v-show="showing" class="row q-mb-sm">
            <div class="col-6 q-pr-sm">
              <SelectField
                v-model="data.agent"
                @clear="() => handleClearAgent(idx)"
                :field="`agents[${idx}].agent`"
                :filterable="true"
                :get-options="getAgentOptions"
                :options-schema="agentOptionsSchema"
                :validation="validators.agent"
                label="Agent"
              />
            </div>
            <div class="q-pl-sm col">
              <SelectField
                v-model="data.legalPersona"
                :disable="!data.agent"
                :field="`agents[${idx}].legalPersona`"
                :filterable="false"
                :get-options="getLegalPersonaOptions"
                :label="data.agent ? 'Legal Persona' : 'Choose an agent'"
                :options-schema="legalPersonaOptionsSchema"
                :validation="validators.legalPersona"
              />
            </div>

            <div class="row items-center">
              <q-btn
                @click.stop="handleRemoveField(idx)"
                class="q-ml-auto"
                icon="clear"
                size="xs"
                flat
                round
                unelevated
              >
              </q-btn>
            </div>
          </div>
        </template>
      </template>
      <template v-else>
        <div class="text-subtitle1 placeholder">
          <p>No named persons.</p>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import { isNil, filter as rFilter, reduce, zip } from "ramda";
import { useFieldArray } from "vee-validate";
import { computed, defineAsyncComponent, defineComponent, ref, unref } from "vue";

import { fetcher, requests } from "@/api";
import { SelectField } from "@/components/forms";
import { agentOptionsSchema, legalPersonaOptionsSchema } from "@/schemas";

import { empty } from "./normalize";

export default defineComponent({
  name: "AgentsField",
  components: {
    SelectField,
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
  },
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    description: {
      type: [Boolean, String],
      default: () => false,
    },
    validators: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:modelValue"],

  setup(props, context) {
    const { fields, replace } = useFieldArray("agents");

    const loading = ref(false);
    const showing = ref(!props.modelValue.length > 0);

    const handleAddField = () => {
      const newValue = [...unref(props.modelValue), empty()];
      context.emit("update:modelValue", newValue);
      replace(newValue);
    };
    const handleRemoveField = (idx) => {
      const newValue = unref(props.modelValue);
      newValue.splice(idx, 1);
      context.emit("update:modelValue", newValue);
      replace(newValue);
    };
    const handleClearAgent = (idx) => {
      const newValue = unref(props.modelValue);
      newValue[idx] = empty();
      context.emit("update:modelValue", newValue);
      replace(newValue);
    };

    const indexed = computed(() => {
      const reducer = (acc, row) => {
        if (!isNil(row.agent)) {
          acc.add(row.agent.value);
        }
        return acc;
      };
      return reduce(reducer, new Set(), props.modelValue);
    });

    const filterAgentOptions = (options) =>
      rFilter((option) => !indexed.value.has(option.id), options);

    const getAgentOptions = () =>
      fetcher(requests.agents.getNamedAgents())
        .then((response) => response.json())
        .then((options) => filterAgentOptions(options));
    const getLegalPersonaOptions = () =>
      fetcher(requests.attributesTypes.getAttributeTypeOptions("legalPersona", true)).then(
        (response) => response.json(),
      );

    return {
      agentOptionsSchema,
      legalPersonaOptionsSchema,
      empty,
      fields,
      filterAgentOptions,
      getAgentOptions,
      getLegalPersonaOptions,
      handleAddField,
      handleClearAgent,
      handleRemoveField,
      loading,
      showing,
      zip,
    };
  },
});
</script>

<style lang="scss" scoped>
.agents-field {
  will-change: auto;
  // will-transform: auto;
}
.agents-field .q-field__after,
.agents-field .q-field__append {
  padding-left: 0 !important;
}
.agents-field .q-field--with-bottom {
  padding-bottom: 0;
}
.agent-select .q-field__native {
  color: black;
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
div.q-dialog__title {
  font-size: 1rem;
}
.separator {
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  padding-bottom: 0.5rem;
}
</style>
