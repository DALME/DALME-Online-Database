<template>
  <SchemaForm :schema="schema" :validation-schema="validationSchema" />
</template>

<script>
import { SchemaFormFactory, useSchemaForm } from "formvuelate";
import VeeValidatePlugin from "@formvuelate/plugin-vee-validate";
import { ref } from "vue";

const SchemaForm = SchemaFormFactory([
  VeeValidatePlugin({
    // plugin configuration here
  }),
]);

export default {
  props: {
    schema: {
      type: Object,
      required: true,
    },
    validationSchema: {
      type: Object,
      required: true,
    },
  },
  components: { SchemaForm },
  setup() {
    const formModel = ref({});

    useSchemaForm(formModel);
  },
};
</script>
