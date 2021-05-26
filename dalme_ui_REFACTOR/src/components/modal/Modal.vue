<template>
  <teleport to="body">
    <div v-show="showModal" class="modal-backdrop">
      <div class="modal-container">
        <div
          ref="modal"
          class="modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-headline"
        >
          <slot></slot>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
import { ref, watch } from "vue";
import { onClickOutside } from "@vueuse/core";

export default {
  name: "Modal",
  props: {
    reauthenticate: {
      type: Function,
      required: true,
    },
    show: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const modal = ref(null);
    const showModal = ref(false);

    const closeModal = () => (showModal.value = false);

    watch(
      () => props.show,
      (show) => {
        showModal.value = show;
      },
    );

    onClickOutside(modal, () => {
      if (showModal.value === true) {
        closeModal();
        props.reauthenticate(false);
      }
    });

    return {
      modal,
      showModal,
    };
  },
};
</script>

<style>
.modal-backdrop {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100%;
  min-width: 100%;
  background: #00000050;
  width: 100%;
  height: auto;
  position: fixed;
  top: 0;
  left: 0;
}
.modal-container {
  display: flex;
  justify-content: center;
  margin-top: 10%;
  text-align: center;
}
.modal {
  background: #fff;
}
</style>
