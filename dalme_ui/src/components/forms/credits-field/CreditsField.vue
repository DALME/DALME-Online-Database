<template>
  <div class="credits-field column q-my-sm" :class="{ separator: !showing }">
    <div class="row items-center q-my-sm">
      <div class="q-field__label no-pointer-events q-mr-auto">
        {{
          !showing && modelValue !== [empty()]
            ? `Credits (${modelValue.length})`
            : "Credits"
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
        <q-tooltip class="bg-blue z-max"> Add a credit </q-tooltip>
      </q-btn>

      <q-btn
        round
        class="q-ml-sm"
        size="xs"
        :icon="showing ? 'visibility_off' : 'visibility'"
        @click.stop="showing = !showing"
      >
        <q-tooltip class="bg-blue z-max">
          {{ showing ? "Hide credits" : "Show credits" }}
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
                :field="`credits[${idx}].agent`"
                :filterable="true"
                :getOptions="getAgentOptions"
                :optionsSchema="agentOptionsSchema"
                :validation="validators.agent"
                v-model="data.agent"
                @clear="() => handleClearAgent(idx)"
              />
            </div>
            <div class="q-pl-sm col-4">
              <SelectField
                :field="`credits[${idx}].role`"
                :disable="!data.agent"
                :label="data.agent ? 'Role' : 'Choose an agent'"
                :filterable="false"
                :getOptions="getRoleOptions(idx)"
                :optionsSchema="creditRoleOptionsSchema"
                :validation="validators.role"
                v-model="data.role"
              />
            </div>
            <div class="q-pl-sm col">
              <div class="row flex-center full-height">
                <q-btn
                  flat
                  round
                  icon="notes"
                  :color="!(data.agent && data.role) ? 'grey' : 'black'"
                  :disable="!(data.agent && data.role)"
                >
                  <q-popup-edit
                    buttons
                    fit
                    anchor="bottom right"
                    class="z-max column"
                    v-model="data.note"
                    :validate="noteValidation"
                    @hide="noteValidation"
                  >
                    <template v-slot="scope">
                      <div class="column">
                        <div class="column">
                          <code
                            class="text-caption text-grey"
                            style="font-size: 0.75rem"
                          >
                            {{ cuid }}
                          </code>
                          <span class="text-caption text-grey-8">
                            {{
                              data.agent && data.role
                                ? `${data.agent.label} (${data.role.label})`
                                : null
                            }}
                          </span>
                        </div>
                        <q-input
                          counter
                          dense
                          autofocus
                          type="textarea"
                          :error="noteError"
                          :error-message="noteErrorMessage"
                          v-model.number="scope.value"
                          @keyup.enter.stop
                        />
                      </div>
                    </template>
                  </q-popup-edit>

                  <q-tooltip class="bg-blue z-max"> Add note </q-tooltip>
                </q-btn>
              </div>
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
          <p>Currently uncredited.</p>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import {
  filter as rFilter,
  isEmpty,
  isNil,
  map as rMap,
  keys,
  reduce,
  zip,
} from "ramda";
import { useFieldArray } from "vee-validate";
import { computed, defineComponent, inject, ref, unref } from "vue";

import { fetcher, requests } from "@/api";
import { SelectField } from "@/components/forms";
import { agentOptionsSchema, creditRoleOptionsSchema } from "@/schemas";

export default defineComponent({
  name: "CreditsField",
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
    const empty = () => ({ agent: null, role: null, note: null });

    const { fields, push, replace } = useFieldArray("credits");

    const cuid = inject("cuid");

    const loading = ref(false);
    const showing = ref(props.modelValue.length > 0 ? true : false);

    const noteError = ref(false);
    const noteErrorMessage = ref("");
    const noteValidation = (val) => {
      if (val && val.length > 255) {
        noteError.value = true;
        noteErrorMessage.value = "Note cannot be longer than 255 characters";
        return false;
      }
      noteError.value = false;
      noteErrorMessage.value = "";
      return true;
    };

    const handleAddField = () => {
      const newValue = unref(props.modelValue);
      context.emit("update:modelValue", [...newValue, empty()]);
      push(empty());
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

    const credited = computed(() => {
      const reducer = (acc, row) => {
        if (row.agent) {
          const agentId = row.agent.value;
          const roleId = isNil(row.role) ? row.role : row.role.value;
          keys(acc).includes(agentId)
            ? acc[agentId].push(roleId)
            : (acc[agentId] = [roleId]);
        }
        return acc;
      };
      return reduce(reducer, {}, props.modelValue);
    });

    const filterRoleOptions = (idx, options) => {
      const agent = props.modelValue[idx].agent;
      if (agent) {
        // Similarly, if an agent is already credited for a role then we need
        // to filter the roles offered as option so that agent can't be
        // credited with the same role more than once.
        const agentId = agent.value;
        const credits = credited.value[agentId];
        return rFilter((option) => !credits.includes(option.id), options);
      }
      return options;
    };
    const filterAgentOptions = (options) => {
      const agents = !isEmpty(credited.value);
      if (agents) {
        // If an agent is registered for all three roles then they shouldn't
        // appear in the options at all.
        const exhausted = keys(
          rFilter((credit) => {
            // TODO: This magic number suggests there's a better way to do all
            // this (filtering of both options lists), but we'll have to come
            // back to that eventually. Probably, we should resolve all the
            // options in onMounted and then go from there, applying filtering
            // at render-time.
            return rMap((value) => Boolean(value), credit).length === 3;
          }, credited.value),
        );
        if (!isEmpty(exhausted)) {
          return rFilter((option) => !exhausted.includes(option.id), options);
        }
      }
      return options;
    };

    const getAgentOptions = () =>
      fetcher(requests.agents.getCreditAgents())
        .then((response) => response.json())
        .then((options) => filterAgentOptions(options));
    const getRoleOptions = (idx) =>
      fetcher(requests.choices.getChoices("Source_credit.type"))
        .then((response) => response.json())
        .then((options) => filterRoleOptions(idx, options));

    return {
      agentOptionsSchema,
      creditRoleOptionsSchema,
      cuid,
      empty,
      fields,
      filterAgentOptions,
      filterRoleOptions,
      getAgentOptions,
      getRoleOptions,
      handleAddField,
      handleClearAgent,
      handleRemoveField,
      loading,
      noteError,
      noteErrorMessage,
      noteValidation,
      showing,
      zip,
    };
  },
});
</script>

<style lang="scss" scoped>
.separator {
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  padding-bottom: 0.5rem;
}
.credits-field .q-field__after,
.credits-field .q-field__append {
  padding-left: 0 !important;
}
.credits-field .q-field--with-bottom {
  padding-bottom: 0;
}
.credit-select .q-field__native {
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
</style>
