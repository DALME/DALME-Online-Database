import { ref, watch } from "vue";

import forms from "@/forms";

export const useDynamicForm = () => {
  const formRequest = ref(null);
  const formSchema = ref(null);
  const validationSchema = ref(null);
  const submitSchema = ref(null);

  const formWatcher = (kind, mode) => {
    watch(
      () => kind.value,
      (value) => {
        if (value) {
          const { submitSchemas, requests, schema, validators } = forms[value];
          formSchema.value = schema;
          formRequest.value = requests[mode.value];
          submitSchema.value = submitSchemas[mode.value];
          validationSchema.value = validators[mode.value];
        } else {
          formSchema.value = null;
          validationSchema.value = null;
        }
      },
      { immediate: true },
    );
  };

  return {
    formSchema,
    formWatcher,
    formRequest,
    submitSchema,
    validationSchema,
  };
};
