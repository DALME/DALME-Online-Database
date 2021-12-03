import { watch } from "vue";

import forms from "@/forms";

export const useForm = () => {
  const formWatcher = (form, formSchema, validationSchema) => {
    watch(
      () => form.value,
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
    );
  };

  return { formWatcher };
};
