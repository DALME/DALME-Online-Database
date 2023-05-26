<template>
  <teleport to="body">
    <div
      :class="`${containerClasses} ${zClass}`"
      ref="el"
      :style="`touch-action:none;${dragging}`"
      v-show="visible"
      @click.stop="handleFocus"
      v-ripple:blue-1
    >
      <q-card borderless class="modal-card">
        <q-card-section :class="`header ${zClass}`">
          <div class="title">{{ modalTitle }}</div>
          <div class="header-button-group">
            <q-btn icon="o_visibility_off" @click.stop="handleMinimize">
              <TooltipWidget> Minimize </TooltipWidget>
            </q-btn>
            <q-btn icon="close" @click.stop="confirm">
              <TooltipWidget> Close </TooltipWidget>
            </q-btn>
          </div>
        </q-card-section>

        <!-- <div class="text-h5 text-capitalize modal-title-slot">
          <slot name="title"></slot>
        </div> -->

        <slot name="content"></slot>
      </q-card>
    </div>
    <q-inner-loading :showing="submitting" />
  </teleport>
</template>

<script>
import { format, useQuasar } from "quasar";
import { computed, defineComponent, ref } from "vue";
import { useDraggable, useStorage } from "@vueuse/core";
import { useActor, useSelector } from "@xstate/vue";
import { useEditing } from "@/use";
import { CustomDialog, TooltipWidget } from "@/components";

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
  components: {
    TooltipWidget,
  },
  setup(props) {
    const $q = useQuasar();
    const { capitalize } = format;
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
    const el = ref(null);
    const ctx = actor.machine.config.context;
    const modalTitle = computed(() =>
      ctx.mode === "create"
        ? `New ${ctx.kind}`
        : `${capitalize(ctx.mode)} ${ctx.initialData.shortName}`,
    );
    const zClass = computed(() =>
      props.cuid === focus.value ? "z-max" : "z-top",
    );
    const containerClasses = computed(() => {
      let classes = ["modal-container"];
      if (props.cuid === focus.value) classes.push("focussed");
      if (valid.value && mouseoverSubmit.value && props.cuid === focus.value)
        classes.push("pulse");
      return classes.join(" ");
    });
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
    const confirm = () => {
      let message = `Do you want to close the window <br />\
        <span class="text-weight-medium">${modalTitle.value}</span>?`;
      if (valid.value)
        /* eslint-disable */
        message =
          message +
          '<br /> <span class="text-red-10 text-weight-medium">\
          Your changes will be lost.</span>';
      /* eslint-enable */
      $q.dialog({
        component: CustomDialog,
        componentProps: {
          isPersistent: true,
          title: "Close window",
          closeIcon: false,
          message: message,
          icon: "disabled_by_default",
          okayButtonLabel: "Close",
          classes: "z-max",
          colourScheme: valid.value ? "warning" : "edit-mode",
        },
      }).onOk(() => {
        send("DESTROY_MODAL", { cuid: props.cuid });
      });
    };

    recenterWatcher(props.cuid, x, y);

    return {
      confirm,
      containerClasses,
      dragging,
      el,
      focus,
      handleFocus,
      handleMinimize,
      modalTitle,
      mouseoverSubmit,
      submitting,
      valid,
      visible,
      zClass,
    };
  },
});
</script>

<style lang="scss" scoped>
.modal-container {
  min-width: 45rem;
  max-width: 50rem;
  position: fixed;
  border-radius: 4px;
  will-change: auto !important;
  box-shadow: rgba(140, 149, 159, 0.2) 0px 8px 24px 0px;
}
.modal-card {
  max-height: calc(100vh - 8rem);
  overflow-y: auto;
  scroll-snap-type: y proximity;
  padding-bottom: 10px;
  border-radius: 4px;
  border-width: 1px;
  border-style: solid;
  border-color: #d1d1d1;
}
.modal-card > div:first-child {
  border-top-left-radius: initial;
  border-top-right-radius: initial;
}
.focussed .modal-card {
  border-color: #c87001;
}
.pulse .modal-card {
  border-color: #c3747c;
}
.header {
  height: 32px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  padding: 0 12px;
  opacity: 1;
  color: #bdbdbd;
  background-color: #f5f5f5;
  border-color: inherit;
  border-bottom-width: 1px;
  border-bottom-style: solid;
}
.focussed .header {
  color: #a85e00;
  background-color: #ffca82;
}
.pulse .header {
  color: #ac0300;
  background-color: #ffccd4;
}
.title {
  font-size: 12px;
  font-weight: 600;
}
.header-button-group {
  display: flex;
  border-color: inherit;
  border-right-width: 1px;
  border-right-style: solid;
  border-left-width: 1px;
  border-left-style: solid;
}
.header-button-group button {
  font-size: 11px;
  padding: 4px;
  height: 30px;
  width: 30px;
  border-color: inherit;
  border-radius: 0;
  border-right-width: 1px;
  border-right-style: dotted;
}
.header-button-group button::before {
  box-shadow: none;
}
.header-button-group button:last-of-type {
  border-right: none;
}
.modal-title-slot {
  background-color: #f5f5f5;
  padding: 10px 15px;
  border-bottom: 1px solid #d1d1d1;
}
</style>
