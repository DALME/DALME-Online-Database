import { watch } from "vue";

import forms from "@/forms";

export const useDynamicForm = (formRequest, formSchema, submitSchema) => {
  const formWatcher = (kind, mode) => {
    watch(
      () => kind.value,
      (value) => {
        if (value) {
          const { form, requests, submit } = forms[value];
          formSchema.value = form;
          formRequest.value = requests[mode.value];
          submitSchema.value = submit[mode.value];
        }
      },
      { immediate: true },
    );
  };

  return {
    formWatcher,
  };
};
