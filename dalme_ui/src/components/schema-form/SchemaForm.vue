<template>
  <q-form>
    <SchemaForm
      v-if="isMultistep"
      :schema="getSubSchema(step)"
      :validation-schema="validator"
      useCustomFormWrapper
    >
      <template v-slot:beforeForm>
        <div class="row">
          <q-btn
            round
            size="sm"
            icon="arrow_back"
            class="q-ml-auto"
            text-color="black"
            :color="!hasPrev ? 'grey' : 'white'"
            :disabled="!hasPrev"
            @click.stop="prevStep"
          />
          <q-btn
            round
            size="sm"
            icon="arrow_forward"
            class="q-ml-sm"
            text-color="black"
            :color="!hasNext ? 'grey' : 'white'"
            :disabled="!hasNext"
            @click.stop="nextStep"
          />
        </div>
      </template>
    </SchemaForm>

    <SchemaForm
      v-else
      :schema="schema"
      :validation-schema="validator"
      useCustomFormWrapper
    />
  </q-form>
</template>

<script>
import { isEmpty } from "ramda";
import { SchemaFormFactory, useSchemaForm } from "formvuelate";
import VeeValidatePlugin from "@formvuelate/plugin-vee-validate";
import { computed, ref, watch } from "vue";
import { useActor } from "@xstate/vue";

import { useEditing } from "@/use";

const SchemaForm = SchemaFormFactory([
  VeeValidatePlugin({
    fieldBagName: "veeValidateFields",
  }),
]);

export default {
  props: {
    cuid: {
      type: String,
      required: true,
    },
    schema: {
      type: Object,
      required: true,
    },
    validator: {
      type: Object,
      required: true,
    },
    formModel: {
      type: Object,
      required: true,
    },
  },
  components: { SchemaForm },
  setup(props) {
    const { forms } = useEditing();

    const step = ref(0);
    const isMultistep = Array.isArray(props.schema);
    const maxSteps = props.schema.length - 1;
    const hasNext = computed(() => step.value < maxSteps);
    const hasPrev = computed(() => step.value > 0);
    const getSubSchema = (step) => {
      if (step <= maxSteps) {
        return props.schema[step];
      }
    };
    const nextStep = () => {
      if (hasNext.value) {
        step.value++;
      }
    };
    const prevStep = () => {
      if (hasPrev.value) {
        step.value--;
      }
    };

    useSchemaForm(props.formModel);

    const cacheFormFields = (data) => {
      const fieldsKey = `form-fields:${props.cuid}`;
      window.localStorage.setItem(fieldsKey, JSON.stringify(data));
    };

    watch(
      () => step.value,
      () => cacheFormFields(props.formModel),
    );

    watch(
      () => props.formModel,
      async (newFormModel) => {
        // Cache the form state for navigation persistence.
        cacheFormFields(newFormModel);

        // We have to do this manually for the time being (Formvuelate can't
        // help us as things currently stand).
        const { send: actorSend } = useActor(forms.value[props.cuid]);
        const isValid = await props.validator.isValid(newFormModel);
        actorSend({ type: "VALIDATE", validated: isValid });
      },
      { deep: true, immediate: true },
    );

    return {
      getSubSchema,
      hasNext,
      hasPrev,
      isEmpty,
      isMultistep,
      nextStep,
      prevStep,
      step,
    };
  },
};
</script>
