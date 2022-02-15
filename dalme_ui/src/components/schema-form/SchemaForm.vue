<template>
  <q-form>
    <SchemaForm :schema="schema" useCustomFormWrapper />
  </q-form>
</template>

<script>
import { SchemaForm, useSchemaForm } from "formvuelate";
import { watch } from "vue";
import { useStorage } from "@vueuse/core";

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

    useSchemaForm(props.formModel);

    watch(
      () => props.formModel,
      async (newFormModel) => {
        // Cache the form state for navigation persistence.
        useStorage(fieldsKey, newFormModel);
      },
      { deep: true, immediate: true },
    );
  },
};
</script>
