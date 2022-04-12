<template>
  <q-form>
    <SchemaForm :schema="schema" useCustomFormWrapper />
  </q-form>
</template>

<script>
import { SchemaForm, useSchemaForm } from "formvuelate";
import { useForm } from "vee-validate";
import { provide, watch } from "vue";
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

    provide("cuid", props.cuid);

    useSchemaForm(props.formModel);
    const { meta } = useForm({
      initialValues: props.formModel,
    });

    watch(
      () => props.formModel,
      (newFormModel) => {
        // Cache the form state for navigation persistence.
        useStorage(fieldsKey, newFormModel, localStorage);
      },
      { deep: true, immediate: true },
    );

    watch(
      () => meta.value,
      async (newMeta) => {
        if (newMeta.touched && !newMeta.pending) {
          const { actor } = forms.value[props.cuid];
          const { send } = useActor(actor);
          send({ type: "VALIDATE", validated: newMeta.valid });
        }
      },
      { deep: true },
    );
  },
};
</script>
