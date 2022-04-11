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
            {{ mode }} {{ kind }}
          </div>
        </q-card-section>

        <SchemaForm :cuid="cuid" :schema="formSchema" :form-model="formModel" />
      </q-card>
    </div>

    <q-dialog v-model="confirm" persistent class="z-max">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="close" color="red" text-color="white" size="sm" />
          <span class="q-ml-sm">Discard form?</span>
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

import { SchemaForm } from "@/components";
import { useAPI, useEditing, useDynamicForm } from "@/use";

export default defineComponent({
  name: "FormModal",
  components: {
    SchemaForm,
  },
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
    const formRequest = ref(null);
    const formSchema = ref(null);
    const submitSchema = ref(null);

    const { apiInterface } = useAPI();
    const { formWatcher } = useDynamicForm(
      formRequest,
      formSchema,
      submitSchema,
    );
    const {
      focus,
      forms,
      formSubmitWatcher,
      mouseoverSubmit,
      recenterWatcher,
      submitting,
      machine: { send },
    } = useEditing();

    const { status, success, fetchAPI } = apiInterface();
    const confirm = ref(false);
    const el = ref(null);

    const { actor } = forms.value[props.cuid];
    const { send: actorSend, state: actorState } = useActor(actor);

    const kind = useSelector(actor, (state) => state.context.kind);
    const mode = useSelector(actor, (state) => state.context.mode);
    const visible = useSelector(actor, (state) => state.context.visible);
    const valid = useSelector(actor, (state) => state.context.validated);
    const initialData = useSelector(
      actor,
      (state) => state.context.initialData,
    );
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

    const fieldsKey = `form-fields:${props.cuid}`;
    const formModel = useStorage(
      fieldsKey,
      initialData.value || {},
      localStorage,
    );

    const handleClose = () => {
      send("DESTROY_MODAL", { cuid: props.cuid });
      formModel.value = null;
      positionValue.value = null;
    };
    const handleFocus = () => send("SET_FOCUS", { value: props.cuid });
    const handleMinimize = () => actorSend("HIDE");

    const handleSubmit = async (postSubmitRefresh) => {
      await submitSchema.value
        .validate(formModel.value, { stripUnknown: true })
        .then(async (value) => {
          const request = formRequest.value(value);
          await fetchAPI(request);
          if (success.value & [200, 201].includes(status.value)) {
            actorSend("RESOLVE");
            postSubmitRefresh.value = true;
            handleClose();
          } else {
            actorSend("REJECT");
          }
        });
    };

    formWatcher(kind, mode);
    formSubmitWatcher(actorState, handleSubmit);
    recenterWatcher(props.cuid, x, y);

    return {
      confirm,
      dragging,
      el,
      focus,
      formModel,
      formSchema,
      handleClose,
      handleFocus,
      handleMinimize,
      isFocus,
      kind,
      mode,
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
  will-change: auto;
}
.modal-card {
  max-height: calc(100vh - 10rem);
  overflow-y: scroll;
  scroll-snap-type: y proximity;
}
</style>
