<template>
  <teleport to="body">
    <div
      class="modal-container"
      :class="isFocus ? 'z-max' : 'z-top'"
      ref="el"
      style="position: fixed"
      :style="dragging"
      v-show="visible"
    >
      <q-card
        class="modal-card q-px-lg q-py-none"
        ref="el"
        :class="{ focussed: cuid === focus }"
        @click="handleFocus"
        v-ripple:blue-3
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

        <SchemaForm :schema="formSchema" :validator="validationSchema" />

        <q-card-actions class="q-px-none q-pb-md">
          <q-btn
            class="q-ml-auto"
            icon="minimize"
            @click.stop="handleMinimize"
            size="11px"
            round
          >
            <q-tooltip self="center left">Minimize</q-tooltip>
          </q-btn>
          <q-btn
            class="q-ml-auto"
            color="deep-orange"
            icon="close"
            @click="handleClose"
            size="11px"
            round
          >
            <q-tooltip self="center left">Discard</q-tooltip>
          </q-btn>
        </q-card-actions>
      </q-card>
    </div>
  </teleport>
</template>

<script>
import { computed, defineComponent, ref } from "vue";
import { useDraggable } from "@vueuse/core";
import { useActor } from "@xstate/vue";

import { SchemaForm } from "@/components";
import { useEditing, useDynamicForm } from "@/use";

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
    const el = ref(null);
    const formSchema = ref(null);
    const validationSchema = ref(null);

    const {
      focus,
      forms,
      formSubmitWatcher,
      machine: { send },
    } = useEditing();
    const { formWatcher } = useDynamicForm();

    const { send: actorSend, state: actorState } = useActor(
      forms.value[props.cuid],
    );
    // TODO: useSelector(actorState, (state) => state.context.kind);
    const kind = computed(() => actorState.value.context.kind);
    const mode = computed(() => actorState.value.context.mode);
    const visible = computed(() => actorState.value.context.visible);
    const isFocus = computed(() => {
      return focus.value === props.cuid;
    });

    const { style: dragging } = useDraggable(el, {
      initialValue: { x: props.xPos, y: props.yPos },
    });

    const handleClose = () => send("DESTROY_FORM", { cuid: props.cuid });
    const handleFocus = () => send("SET_FOCUS", { value: props.cuid });
    const handleMinimize = () => actorSend("HIDE");
    const handleSubmit = () => console.log("KLAXON");

    formSubmitWatcher(actorState, handleSubmit);
    formWatcher(kind, formSchema, validationSchema);

    return {
      dragging,
      el,
      focus,
      formSchema,
      handleClose,
      handleFocus,
      handleMinimize,
      isFocus,
      kind,
      mode,
      validationSchema,
      visible,
    };
  },
});
</script>

<style lang="scss" scoped>
.focussed {
  border-radius: 0;
  border: 3px solid green;
}
.modal-container {
  border: 1px solid #ccc;
  box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
  min-width: 20rem;
}
.modal-card {
  overflow-y: scroll;
  scroll-snap-type: y proximity;
  max-height: 30rem;
}
</style>
