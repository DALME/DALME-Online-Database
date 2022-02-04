<template>
  <q-form>
    <SchemaForm
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
import { watch } from "vue";
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

    useSchemaForm(props.formModel);

    const cacheFormFields = (data) => {
      const fieldsKey = `form-fields:${props.cuid}`;
      window.localStorage.setItem(fieldsKey, JSON.stringify(data));
    };

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
      isEmpty,
    };
  },
};
</script>
