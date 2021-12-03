<template>
  <SchemaForm
    :schema="schema"
    :validation-schema="validator"
    @submit="onSubmit"
  />
</template>

<script>
import { SchemaFormFactory, useSchemaForm } from "formvuelate";
import VeeValidatePlugin from "@formvuelate/plugin-vee-validate";
import { ref } from "vue";

const SchemaForm = SchemaFormFactory([
  VeeValidatePlugin({
    // Plugin configuration goes here.
  }),
]);

export default {
  props: {
    schema: {
      type: Object,
      required: true,
    },
    validator: {
      type: Object,
      required: true,
    },
  },
  components: { SchemaForm },
  setup() {
    const formModel = ref({});

    useSchemaForm(formModel);

    const onSubmit = () => null;

    return {
      onSubmit,
    };
  },
};
</script>
