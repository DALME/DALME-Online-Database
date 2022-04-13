<template>
  <teleport to="body">
    <div
      class="modal-container"
      ref="el"
      :class="isFocus ? 'z-max' : 'z-top'"
      :style="`touch-action:none;${dragging}`"
      v-show="visible"
      @click.stop="handleFocus"
      v-ripple:blue-1
    >
      <q-card
        class="modal-card q-px-md q-pt-none q-pb-md"
        :class="{
          focussed: cuid === focus,
          pulse: valid && mouseoverSubmit && cuid === focus,
        }"
      >
        <q-card-section class="q-px-none q-pt-sm">
          <div class="row no-wrap flex-center q-pb-sm">
            <span class="text-caption text-grey">
              <code>{{ cuid }}</code>
            </span>
            <q-btn
              round
              class="q-ml-auto"
              icon="minimize"
              size="xs"
              @click.stop="handleMinimize"
            >
              <q-tooltip class="bg-blue z-max"> Minimize </q-tooltip>
            </q-btn>
            <q-btn
              round
              class="q-ml-xs"
              color="deep-orange"
              icon="close"
              size="xs"
              @click.stop="confirm = true"
            >
              <q-tooltip class="bg-blue z-max"> Discard </q-tooltip>
            </q-btn>
          </div>
          <div class="text-h5 text-capitalize text-bold">
            <slot name="title"></slot>
          </div>
        </q-card-section>

        <slot name="content"></slot>
      </q-card>
    </div>

    <q-dialog v-model="confirm" persistent class="z-max">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="close" color="red" text-color="white" size="sm" />
          <span class="q-ml-sm">Close?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn
            flat
            label="Discard"
            color="primary"
            v-close-popup
            @click.stop="handleClose"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-inner-loading :showing="submitting" />
  </teleport>
</template>

<script>
import { computed, defineComponent, ref } from "vue";
import { useDraggable, useStorage } from "@vueuse/core";
import { useActor, useSelector } from "@xstate/vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "BaseModal",
  props: {
    cuid: {
      type: String,
      required: true,
    },
    xPos: {
      type: Number,
      required: true,
    },
    yPos: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const {
      focus,
      modals,
      mouseoverSubmit,
      recenterWatcher,
      submitting,
      machine: { send },
    } = useEditing();

    const { actor } = modals.value[props.cuid];
    const { send: actorSend } = useActor(actor);
    const visible = useSelector(actor, (state) => state.context.visible);
    const valid = useSelector(actor, (state) => state.context.validated);

    const confirm = ref(false);
    const el = ref(null);
    const isFocus = computed(() => focus.value === props.cuid);
    const positionKey = `form-position:${props.cuid}`;
    const positionValue = useStorage(
      positionKey,
      { x: props.xPos, y: props.yPos },
      localStorage,
    );
    const {
      x,
      y,
      style: dragging,
    } = useDraggable(el, {
      initialValue: positionValue,
      onEnd: () => useStorage(positionKey, { x, y }, localStorage),
    });

    const handleFocus = () => send("SET_FOCUS", { value: props.cuid });
    const handleMinimize = () => actorSend("HIDE");
    const handleClose = () => {
      send("DESTROY_MODAL", { cuid: props.cuid });
    };

    recenterWatcher(props.cuid, x, y);

    return {
      confirm,
      dragging,
      el,
      focus,
      handleClose,
      handleFocus,
      handleMinimize,
      isFocus,
      mouseoverSubmit,
      submitting,
      valid,
      visible,
    };
  },
});
</script>

<style lang="scss" scoped>
.focussed {
  border-radius: 0;
  border-left: 4px solid green;
  transition: border 0.05s linear;
}
.pulse {
  border-left: 8px solid red;
  transition: border 0.5s linear;
}
.modal-container {
  box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
  min-width: 40rem;
  max-width: 45rem;
  position: fixed;
  will-change: auto !important;
}
.modal-card {
  max-height: calc(100vh - 10rem);
  overflow-y: scroll;
  scroll-snap-type: y proximity;
}
</style>
