<template>
  <transition
    :duration="2000"
    appear
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
  >
    <q-page-sticky position="bottom-right" :offset="position" class="z-max">
      <q-btn
        fab
        :disable="disabled"
        @click="submitTransport"
        color="green"
        icon="save"
        v-touch-pan.prevent.mouse="drag"
      />
    </q-page-sticky>
  </transition>
</template>

<script>
import { computed, defineComponent, inject, ref } from "vue";

export default defineComponent({
  name: "TransportSubmit",
  setup(_, context) {
    const enableSave = inject("enableSave");
    const submitted = ref(false);
    const position = ref([30, 30]);
    const dragging = ref(false);
    const disabled = computed(
      () => (submitted.value || dragging.value) && !enableSave.value,
    );

    const submitTransport = () => {
      submitted.value = true;
      enableSave.value = false;
      context.emit("submitTransport");
    };

    const drag = (event) => {
      dragging.value = event.isFirst !== true && event.isFinal !== true;
      position.value = [
        position.value[0] - event.delta.x,
        position.value[1] - event.delta.y,
      ];
    };

    return {
      drag,
      disabled,
      position,
      submitTransport,
    };
  },
});
</script>
