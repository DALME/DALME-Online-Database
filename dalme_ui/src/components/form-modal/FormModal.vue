<template>
  <teleport to="body">
    <UseDraggable
      class="modal-container"
      :class="isFocus ? 'z-max' : 'z-top'"
      :initialValue="initialPosition"
      :storage-key="positionKey"
      storage-type="session"
      style="position: fixed"
      v-show="visible"
    >
      <q-card
        class="modal-card q-px-lg q-py-none"
        :class="{
          focussed: cuid === focus,
          pulse: !disabled && mouseoverSubmit && cuid === focus,
        }"
        @click="handleFocus"
        v-ripple:blue-1
      >
        <q-card-section class="q-px-none q-pt-sm">
          <div class="row no-wrap items-center q-pb-sm">
            <span class="text-caption text-grey">
              <code>{{ cuid }}</code>
            </span>
          </div>
          <div class="text-h5 text-capitalize text-bold">
            {{ mode }} {{ kind }}
          </div>
        </q-card-section>

        <SchemaForm
          :cuid="cuid"
          :schema="formSchema"
          :validator="validationSchema"
          :formModel="formModel"
        />

        <q-card-actions class="q-mt-md q-px-none q-pb-md">
          <q-btn
            class="q-ml-auto"
            icon="minimize"
            @click.stop="handleMinimize"
            size="11px"
            round
          >
            <q-tooltip class="bg-blue z-max"> Minimize </q-tooltip>
          </q-btn>
          <q-btn
            class="q-ml-auto"
            color="deep-orange"
            icon="close"
            @click="confirm = true"
            size="11px"
            round
          >
            <q-tooltip class="bg-blue z-max"> Discard </q-tooltip>
          </q-btn>
        </q-card-actions>
      </q-card>
    </UseDraggable>

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
            @click="handleClose"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-inner-loading :showing="submitting" />
  </teleport>
</template>

<script>
import { computed, defineComponent, ref } from "vue";
import { UseDraggable } from "@vueuse/components";
import { useActor, useSelector } from "@xstate/vue";

import { SchemaForm } from "@/components";
import { useAPI, useEditing, useDynamicForm } from "@/use";

export default defineComponent({
  name: "FormModal",
  components: {
    SchemaForm,
    UseDraggable,
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
  setup(props, context) {
    const { data, status, success, fetchAPI } = useAPI(context);
    const {
      formRequest,
      formSchema,
      formWatcher,
      validationSchema,
      submitSchema,
    } = useDynamicForm();
    const {
      disabled,
      focus,
      forms,
      formSubmitWatcher,
      mouseoverSubmit,
      submitting,
      machine: { send },
    } = useEditing();

    const confirm = ref(false);

    const actor = forms.value[props.cuid];
    const { send: actorSend, state: actorState } = useActor(actor);

    const kind = useSelector(actor, (state) => state.context.kind);
    const mode = useSelector(actor, (state) => state.context.mode);
    const visible = useSelector(actor, (state) => state.context.visible);
    const initialData = useSelector(
      actor,
      (state) => state.context.initialData,
    );
    const isFocus = computed(() => focus.value === props.cuid);

    const positionKey = `form-position:${props.cuid}`;
    const initialPosition = { x: props.xPos, y: props.yPos };

    const fieldsKey = `form-fields:${props.cuid}`;
    const formModel = ref(
      initialData.value || JSON.parse(localStorage.getItem(fieldsKey)) || {},
    );

    const handleClose = () => {
      send("DESTROY_FORM", { cuid: props.cuid });
      window.localStorage.removeItem(positionKey);
      window.localStorage.removeItem(fieldsKey);
    };
    const handleFocus = () => send("SET_FOCUS", { value: props.cuid });
    const handleMinimize = () => actorSend("HIDE");

    const handleSubmit = async () => {
      await submitSchema.value
        .validate(formModel.value, { stripUnknown: true })
        .then(async (value) => {
          const request = formRequest.value(value);
          await fetchAPI(request);
          if (success.value & [200, 201].includes(status.value)) {
            // const message = `${kind.value} ${mode.value}d`;
            actorSend("RESOLVE"); // send("RESOLVE", { cuid: props.cuid, messsage });
            handleClose();
          } else {
            actorSend("REJECT"); // send("REJECT", { cuid: props.cuid, message });
          }
        });
    };

    formWatcher(kind, mode);
    formSubmitWatcher(actorState, handleSubmit); // TODO: Use the service not the state.

    return {
      confirm,
      disabled,
      focus,
      formModel,
      formSchema,
      handleClose,
      handleFocus,
      handleMinimize,
      initialPosition,
      isFocus,
      kind,
      mode,
      mouseoverSubmit,
      positionKey,
      submitting,
      validationSchema,
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
  width: 25rem;
}
.modal-card {
  overflow-y: scroll;
  scroll-snap-type: y proximity;
  max-height: 30rem;
}
</style>
