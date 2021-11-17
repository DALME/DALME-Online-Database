import { computed, inject, provide, toRefs, watch } from "vue";

const EditingSymbol = Symbol();

export const provideEditing = (editing) => {
  const { detail, enableSave, form, locked, mode, submitting } =
    toRefs(editing);

  const showFormModal = computed(() => mode.value === "form");

  const resetEditing = () => {
    form.value = null;
    locked.value = false;
    mode.value = null;
    enableSave.value = false;
    submitting.value = false;
  };

  const editingSubmitWatcher = (handleSubmit) => {
    watch(
      () => submitting.value,
      async (value) => {
        if (value) {
          await handleSubmit();
          // Handle all resetting *inside* the handleSubmit callback so we can
          // account for errors and other execution details.
        }
      },
    );
  };

  // Expects a computed property reporting on whether or not some form has been
  // touched by the user. Allows us to disable CRUD controls conditionally.
  // Also informs us which form of CRUD we are engaged in, inline or form.
  const isEditingWatcher = (isDirty, inMode) => {
    watch(
      () => isDirty.value,
      (value) => {
        locked.value = value;
        mode.value = value ? inMode : null;
      },
    );
  };

  provide(EditingSymbol, {
    detail,
    editingSubmitWatcher,
    enableSave,
    form,
    isEditingWatcher,
    locked,
    mode, // Will expose funcs to manipulate this eventually.
    resetEditing,
    showFormModal,
    submitting,
  });
};

export const useEditing = () => inject(EditingSymbol);
