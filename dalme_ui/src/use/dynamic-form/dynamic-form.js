import { watch } from "vue";

import forms from "@/forms";

export const useDynamicForm = () => {
  const formWatcher = (kind, formSchema, validationSchema) => {
    watch(
      () => kind.value,
      (value) => {
        if (value) {
          const { schema, validator } = forms[value];
          formSchema.value = schema;
          validationSchema.value = validator;
        } else {
          formSchema.value = null;
          validationSchema.value = null;
        }
      },
      { immediate: true },
    );
  };

  return { formWatcher };
};
