<template>
  <div class="agents-field column q-my-sm" :class="{ separator: !showing }">
    <div class="row items-center q-my-sm">
      <div class="q-field__label no-pointer-events q-mr-auto">
        {{
          !showing && modelValue !== [empty()]
            ? `Named persons (${modelValue.length})`
            : "Named persons"
        }}
      </div>

      <q-spinner v-if="loading" color="primary" size="xs" />
      <q-btn
        v-show="showing"
        round
        class="q-ml-sm"
        color="amber"
        icon="add"
        size="xs"
        text-color="black"
        @click.stop="handleAddField"
      >
        <q-tooltip class="bg-blue z-max"> Add a named person </q-tooltip>
      </q-btn>

      <q-btn
        round
        class="q-ml-sm"
        size="xs"
        :icon="showing ? 'visibility_off' : 'visibility'"
        @click.stop="showing = !showing"
      >
        <q-tooltip class="bg-blue z-max">
          {{ showing ? "Hide named persons" : "Show named persons" }}
        </q-tooltip>
      </q-btn>
    </div>

    <template v-if="showing">
      <template v-if="modelValue.length > 0">
        <template
          v-for="({ 0: data, 1: field }, idx) in zip(modelValue, fields)"
          :key="field.key"
        >
          <div class="row q-mb-sm" v-show="showing">
            <div class="col-6 q-pr-sm">
              <SelectField
                label="Agent"
                :field="`agents[${idx}].agent`"
                :filterable="true"
                :getOptions="getAgentOptions"
                :optionsSchema="agentOptionsSchema"
                :validation="validators.agent"
                v-model="data.agent"
                @clear="() => handleClearAgent(idx)"
              />
            </div>
            <div class="q-pl-sm col">
              <SelectField
                :field="`agents[${idx}].legalPersona`"
                :disable="!data.agent"
                :label="data.agent ? 'Legal Persona' : 'Choose an agent'"
                :filterable="false"
                :getOptions="getLegalPersonaOptions"
                :optionsSchema="legalPersonaOptionsSchema"
                :validation="validators.legalPersona"
                v-model="data.legalPersona"
              />
            </div>

            <div class="row items-center">
              <q-btn
                class="q-ml-auto"
                flat
                round
                unelevated
                size="xs"
                icon="clear"
                @click.stop="handleRemoveField(idx)"
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
import { filter as rFilter, isNil, reduce, zip } from "ramda";
import { useFieldArray } from "vee-validate";
import { computed, defineComponent, ref, unref } from "vue";

import { fetcher, requests } from "@/api";
import { SelectField } from "@/components/forms";
import { agentOptionsSchema, legalPersonaOptionsSchema } from "@/schemas";

import { empty } from "./normalize";

export default defineComponent({
  name: "AgentsField",
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    validators: {
      type: Object,
      required: true,
    },
  },
  components: {
    SelectField,
  },
  setup(props, context) {
    const { fields, replace } = useFieldArray("agents");

    const loading = ref(false);
    const showing = ref(props.modelValue.length > 0 ? true : false);

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
      fetcher(requests.attributes.getAttributeOptions("legalPersona")).then(
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
  will-transform: auto;
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
