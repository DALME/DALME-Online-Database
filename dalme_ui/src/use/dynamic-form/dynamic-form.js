import { ref, watch } from "vue";

import forms from "@/forms";

export const useDynamicForm = () => {
  const formRequest = ref(null);
  const formSchema = ref(null);
  const submitSchema = ref(null);

  const formWatcher = (kind, mode) => {
    watch(
      () => kind.value,
      (value) => {
        if (value) {
          const { requests, form, submit } = forms[value];
          formSchema.value = form;
          formRequest.value = requests[mode.value];
          submitSchema.value = submit[mode.value];
        } else {
          formSchema.value = null;
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
  };
};
