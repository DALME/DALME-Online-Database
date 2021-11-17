<template>
  <teleport to="body">
    <!-- TODO: transition of some kind -->
    <!-- TODO: probably want to use slots to accept the form itself. -->
    <q-card v-if="showFormModal" class="modal-container column z-top">
      <h3>{{ kind }} form</h3>
      <q-btn class="q-mt-lg" :onClick="handleClose">Close</q-btn>
    </q-card>
  </teleport>
</template>

<script>
import { computed, defineComponent } from "vue";
import { useEditing } from "@/use";

export default defineComponent({
  name: "FormModal",
  setup() {
    const { form, resetEditing, showFormModal } = useEditing();
    const kind = computed(() =>
      form.value
        ? form.value.charAt(0).toUpperCase() + form.value.slice(1)
        : null,
    );

    const handleClose = () => resetEditing();

    return {
      handleClose,
      kind,
      showFormModal,
    };
  },
});
</script>

<style lang="scss">
.modal-container {
  box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 12rem;
  background: white;
  border: 1px solid;
}
</style>
