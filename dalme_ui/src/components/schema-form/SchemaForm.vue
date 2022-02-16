<template>
  <q-form>
    <SchemaForm :schema="schema" useCustomFormWrapper />
  </q-form>
</template>

<script>
import { SchemaForm, useSchemaForm } from "formvuelate";
import { watch } from "vue";
import { useForm } from "vee-validate";
import { useStorage } from "@vueuse/core";
import { useActor } from "@xstate/vue";

import { useEditing } from "@/use";

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
    formModel: {
      type: Object,
      required: true,
    },
  },
  components: { SchemaForm },
  setup(props) {
    const fieldsKey = `form-fields:${props.cuid}`;
    const { forms } = useEditing();

    const { errors, meta } = useForm();
    useSchemaForm(props.formModel);

    watch(
      () => props.formModel,
      (newFormModel) => {
        // Cache the form state for navigation persistence.
        useStorage(fieldsKey, newFormModel, localStorage);
      },
      { deep: true, immediate: true },
    );

    // TODO: Remove this, is useful for dev
    watch(
      () => errors.value,
      (newErrors) => {
        console.log(newErrors);
      },
    );

    watch(
      () => meta.value,
      (newMeta) => {
        const { send } = useActor(forms.value[props.cuid]);
        send({ type: "VALIDATE", validated: newMeta.valid });
      },
    );
  },
};
</script>
