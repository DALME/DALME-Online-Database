<template>
  <teleport to="body">
    <div
      v-if="showFormModal"
      class="modal-container column z-top"
      ref="el"
      style="position: fixed"
      :style="style"
    >
      <SchemaForm :schema="formSchema" :validator="validationSchema" />
      <q-btn class="q-mt-lg" icon="close" :onClick="handleClose" />
    </div>
  </teleport>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useDraggable } from "@vueuse/core";

import { SchemaForm } from "@/components";
import { useEditing, useForm } from "@/use";

export default defineComponent({
  name: "FormModal",
  components: {
    SchemaForm,
  },
  setup() {
    const el = ref(null);
    const formSchema = ref(null);
    const validationSchema = ref(null);

    const { form, resetEditing, showFormModal } = useEditing();
    const { formWatcher } = useForm(form);
    const { style } = useDraggable(el, {
      initialValue: { x: 400, y: 2 },
    });

    formWatcher(form, formSchema, validationSchema);

    const handleClose = () => resetEditing();

    return {
      el,
      formSchema,
      handleClose,
      showFormModal,
      style,
      validationSchema,
    };
  },
});
</script>

<style lang="scss">
.modal-container {
  border: 1px solid #ccc;
  box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
  padding: 2rem 12rem;
  background: white;
}
</style>
